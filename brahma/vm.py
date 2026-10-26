"""The BRAHMA stack virtual machine.

The VM executes :class:`~brahma.bytecode.CodeObject` images produced by the
compiler.  It is deliberately small and dependency free, but it is a *real*
VM: it has frames, locals, a value stack, jump patching, function objects,
recursion, a step budget and precise runtime diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .bytecode import CodeObject, Instruction
from .errors import RuntimeFault

DEFAULT_STEP_LIMIT = 1_000_000
DEFAULT_MAX_DEPTH = 500


class Function:
    """A user defined function: code plus its captured lexical scope."""

    __slots__ = ("code", "globals", "closure")

    def __init__(
        self,
        code: CodeObject,
        globals_: Dict[str, Any],
        closure: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.code = code
        self.globals = globals_
        #: Enclosing scopes, innermost first.  Capturing the *live* dicts is
        #: what makes closures observe later assignments to captured names.
        self.closure = list(closure or [])

    @property
    def name(self) -> str:
        return self.code.name

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return "<function %s(%s)>" % (self.name, ", ".join(self.code.params))


class Builtin:
    """A native function exposed to BRAHMA programs."""

    __slots__ = ("name", "func", "min_args", "max_args")

    def __init__(self, name: str, func: Callable, min_args: int, max_args: Optional[int]) -> None:
        self.name = name
        self.func = func
        self.min_args = min_args
        self.max_args = max_args

    def __call__(self, *args: Any) -> Any:
        return self.func(*args)

    def check_arity(self, count: int) -> None:
        if count < self.min_args or (self.max_args is not None and count > self.max_args):
            if self.max_args is None:
                expected = "कम से कम %d" % self.min_args
            elif self.min_args == self.max_args:
                expected = "%d" % self.min_args
            else:
                expected = "%d-%d" % (self.min_args, self.max_args)
            raise RuntimeFault(
                "'%s' को %s आर्ग्युमेंट चाहिए, %d मिले" % (self.name, expected, count)
            )


@dataclass
class Frame:
    """One activation record."""

    code: CodeObject
    ip: int = 0
    stack: List[Any] = field(default_factory=list)
    locals: Dict[str, Any] = field(default_factory=dict)
    last_line: int = 0
    #: Enclosing lexical scopes, innermost first (closures).
    enclosing: List[Dict[str, Any]] = field(default_factory=list)
    #: Active ``प्रयास`` guards as ``(handler_ip, stack_depth, name)``.
    handlers: List[Any] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.code.name


def truthy(value: Any) -> bool:
    """BRAHMA truthiness: ``0``, ``""``, ``[]``, ``None`` and ``false`` are false."""
    if value is None or value is False:
        return False
    if isinstance(value, (int, float)) and value == 0:
        return False
    if isinstance(value, (str, list, tuple, dict)) and len(value) == 0:
        return False
    return True


def format_value(value: Any) -> str:
    """Render a value the way ``दर्शय`` prints it."""
    if value is None:
        return "शून्य"
    if value is True:
        return "सत्य"
    if value is False:
        return "असत्य"
    if isinstance(value, float):
        if value == int(value) and abs(value) < 1e16:
            return "%d.0" % int(value)
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(format_value(item) for item in value) + "]"
    if isinstance(value, dict):
        pairs = ["%s: %s" % (format_value(key), format_value(item))
                 for key, item in value.items()]
        return "{" + ", ".join(pairs) + "}"
    if isinstance(value, Function):  # pragma: no cover - printing a function
        return "<कार्य %s>" % value.name
    if isinstance(value, Builtin):  # pragma: no cover
        return "<निविड़ कार्य %s>" % value.name
    return str(value)


def _builtin_len(value: Any) -> int:
    if not isinstance(value, (str, list, tuple, dict)):
        raise RuntimeFault("लम्बाई() केवल शब्द/सूची पर लागू है")
    return len(value)


def _builtin_int(value: Any = 0) -> int:
    try:
        if isinstance(value, str):
            return int(value.strip())
        return int(value)
    except (TypeError, ValueError):
        raise RuntimeFault("संख्या() में अमान्य मान: %r" % (value,))


def _builtin_float(value: Any = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise RuntimeFault("दशमलव() में अमान्य मान: %r" % (value,))


def _builtin_str(value: Any = "") -> str:
    return format_value(value)


def _builtin_bool(value: Any = False) -> bool:
    return truthy(value)


def _builtin_abs(value: Any) -> Any:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise RuntimeFault("निरपेक्ष() को संख्या चाहिए")
    return abs(value)


def _builtin_min(*args: Any) -> Any:
    values = list(args[0]) if len(args) == 1 and isinstance(args[0], (list, tuple)) else list(args)
    if not values:
        raise RuntimeFault("न्यूनतम() को खाली सूची नहीं चाहिए")
    return min(values)


def _builtin_max(*args: Any) -> Any:
    values = list(args[0]) if len(args) == 1 and isinstance(args[0], (list, tuple)) else list(args)
    if not values:
        raise RuntimeFault("अधिकतम() को खाली सूची नहीं चाहिए")
    return max(values)


def _builtin_range(*args: Any) -> List[int]:
    try:
        return list(range(*(int(arg) for arg in args)))
    except (TypeError, ValueError):
        raise RuntimeFault("श्रेणी() में अमान्य मान")


def _builtin_join(separator: Any, items: Any) -> str:
    if not isinstance(separator, str) or not isinstance(items, list):
        raise RuntimeFault("जोड़ो() को (शब्द, सूची) चाहिए")
    return separator.join(format_value(item) for item in items)


def _builtin_append(items: Any, value: Any) -> List[Any]:
    if not isinstance(items, list):
        raise RuntimeFault("जोड़ें() को सूची चाहिए")
    items.append(value)
    return items


def _builtin_push(items: Any, value: Any) -> List[Any]:  # pragma: no cover - alias
    return _builtin_append(items, value)


# --- strings -------------------------------------------------------------
def _need_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise RuntimeFault("%s() को शब्द चाहिए, मिला %s" % (name, type(value).__name__))
    return value


def _builtin_split(text: Any, separator: Any = None) -> List[str]:
    text = _need_str(text, "विभाजन")
    if separator is None:
        return text.split()
    if not isinstance(separator, str):
        raise RuntimeFault("विभाजन() का विभाजक शब्द होना चाहिए")
    if separator == "":
        raise RuntimeFault("विभाजन() का विभाजक खाली नहीं हो सकता")
    return text.split(separator)


def _builtin_replace(text: Any, old: Any, new: Any) -> str:
    return _need_str(text, "प्रतिस्थापन").replace(_need_str(old, "प्रतिस्थापन"),
                                                  _need_str(new, "प्रतिस्थापन"))


def _builtin_trim(text: Any) -> str:
    return _need_str(text, "त्रिम").strip()


def _builtin_upper(text: Any) -> str:
    return _need_str(text, "बड़े").upper()


def _builtin_lower(text: Any) -> str:
    return _need_str(text, "छोटे").lower()


def _builtin_find(text: Any, needle: Any) -> int:
    return _need_str(text, "खोज").find(_need_str(needle, "खोज"))


def _builtin_str_repeat(text: Any, count: Any) -> str:
    text = _need_str(text, "दोहराओ")
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise RuntimeFault("दोहराओ() की संख्या अऋणात्मक पूर्णांक होनी चाहिए")
    return text * count


# --- lists ---------------------------------------------------------------
def _need_list(value: Any, name: str) -> list:
    if not isinstance(value, list):
        raise RuntimeFault("%s() को सूची चाहिए, मिला %s" % (name, type(value).__name__))
    return value


def _builtin_sort(items: Any) -> List[Any]:
    values = _need_list(items, "क्रम")
    try:
        return sorted(values)
    except TypeError:
        raise RuntimeFault("क्रम() — मिश्रित प्रकारों को क्रम में नहीं लगाया जा सकता")


def _builtin_reverse(items: Any) -> List[Any]:
    return list(reversed(_need_list(items, "उलटा")))


def _builtin_pop(items: Any, index: Any = -1) -> Any:
    values = _need_list(items, "हटाओ")
    if isinstance(index, bool) or not isinstance(index, int):
        raise RuntimeFault("हटाओ() का सूचकांक पूर्णांक होना चाहिए")
    if not values:
        raise RuntimeFault("हटाओ() — सूची खाली है")
    try:
        return values.pop(index)
    except IndexError:
        raise RuntimeFault("हटाओ() — सूचकांक सीमा से बाहर")


def _builtin_insert(items: Any, index: Any, value: Any) -> List[Any]:
    values = _need_list(items, "सम्मिलित")
    if isinstance(index, bool) or not isinstance(index, int):
        raise RuntimeFault("सम्मिलित() का सूचकांक पूर्णांक होना चाहिए")
    values.insert(index, value)
    return values


def _builtin_extend(items: Any, other: Any) -> List[Any]:
    values = _need_list(items, "विस्तार")
    values.extend(_need_list(other, "विस्तार"))
    return values


def _builtin_count(items: Any, value: Any) -> int:
    if isinstance(items, str):
        return items.count(_need_str(value, "गिनती"))
    return _need_list(items, "गिनती").count(value)


def _builtin_index_of(items: Any, value: Any) -> int:
    if isinstance(items, str):
        return items.find(_need_str(value, "स्थान"))
    values = _need_list(items, "स्थान")
    try:
        return values.index(value)
    except ValueError:
        raise RuntimeFault("स्थान() — मान सूची में नहीं है")


def _builtin_sum(items: Any) -> Any:
    values = _need_list(items, "योगफल")
    total: Any = 0
    for item in values:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise RuntimeFault("योगफल() केवल संख्याओं पर लागू है")
        total += item
    return total


def _builtin_list(value: Any = None) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, (list, str, tuple)):
        return list(value)
    if isinstance(value, dict):
        return list(value.keys())
    raise RuntimeFault("सूची() इस मान से सूची नहीं बना सकता")


# --- dicts ---------------------------------------------------------------
def _need_dict(value: Any, name: str) -> dict:
    if not isinstance(value, dict):
        raise RuntimeFault("%s() को तालिका चाहिए, मिला %s" % (name, type(value).__name__))
    return value


def _builtin_keys(table: Any) -> List[Any]:
    return list(_need_dict(table, "कुंजियाँ").keys())


def _builtin_values(table: Any) -> List[Any]:
    return list(_need_dict(table, "मान").values())


def _builtin_has(table: Any, key: Any) -> bool:
    return key in _need_dict(table, "समाविष्ट")


def _builtin_drop(table: Any, key: Any) -> Any:
    mapping = _need_dict(table, "हटाओ_कुंजी")
    if key not in mapping:
        raise RuntimeFault("हटाओ_कुंजी() — कुंजी नहीं मिली: %r" % (key,))
    return mapping.pop(key)


def _builtin_dict() -> Dict[Any, Any]:
    return {}


# --- maths / misc --------------------------------------------------------
def _builtin_sqrt(value: Any) -> float:
    import math as _math

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RuntimeFault("वर्गमूल() को संख्या चाहिए")
    if value < 0:
        raise RuntimeFault("वर्गमूल() ऋणात्मक संख्या पर परिभाषित नहीं")
    return _math.sqrt(value)


def _builtin_type(value: Any) -> str:
    if value is None:
        return "शून्य"
    if isinstance(value, bool):
        return "बूलियन"
    if isinstance(value, int):
        return "पूर्णांक"
    if isinstance(value, float):
        return "दशमलव"
    if isinstance(value, str):
        return "शब्द"
    if isinstance(value, list):
        return "सूची"
    if isinstance(value, dict):
        return "तालिका"
    return "अन्य"


def _builtin_round(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RuntimeFault("गोल() को संख्या चाहिए")
    return int(round(value))


def _builtin_sorted_join(items: Any) -> str:
    return "".join(format_value(item) for item in _need_list(items, "मिलाओ"))


#: The standard library exposed to every program.
BUILTINS: Dict[str, Builtin] = {}


def _register(names, func, min_args, max_args) -> None:
    builtin = Builtin(names[0], func, min_args, max_args)
    for name in names:
        BUILTINS[name] = builtin


_register(("लम्बाई", "len"), _builtin_len, 1, 1)
_register(("संख्या", "int"), _builtin_int, 1, 1)
_register(("दशमलव", "float"), _builtin_float, 1, 1)
_register(("पाठ", "str"), _builtin_str, 1, 1)
_register(("सत्यता", "bool"), _builtin_bool, 1, 1)
_register(("निरपेक्ष", "abs"), _builtin_abs, 1, 1)
_register(("न्यूनतम", "min"), _builtin_min, 1, None)
_register(("अधिकतम", "max"), _builtin_max, 1, None)
_register(("श्रेणी", "range"), _builtin_range, 1, 3)
_register(("जोड़ो", "join"), _builtin_join, 2, 2)
_register(("जोड़ें", "append"), _builtin_append, 2, 2)
_register(("विभाजन", "split"), _builtin_split, 1, 2)
_register(("प्रतिस्थापन", "replace"), _builtin_replace, 3, 3)
_register(("त्रिम", "trim", "strip"), _builtin_trim, 1, 1)
_register(("बड़े", "upper"), _builtin_upper, 1, 1)
_register(("छोटे", "lower"), _builtin_lower, 1, 1)
_register(("खोज", "find"), _builtin_find, 2, 2)
_register(("दोहराओ", "repeat"), _builtin_str_repeat, 2, 2)
_register(("क्रम", "sort", "sorted"), _builtin_sort, 1, 1)
_register(("उलटा", "reverse"), _builtin_reverse, 1, 1)
_register(("हटाओ", "pop"), _builtin_pop, 1, 2)
_register(("सम्मिलित", "insert"), _builtin_insert, 3, 3)
_register(("विस्तार", "extend"), _builtin_extend, 2, 2)
_register(("गिनती", "count"), _builtin_count, 2, 2)
_register(("स्थान", "index_of"), _builtin_index_of, 2, 2)
_register(("योगफल", "sum"), _builtin_sum, 1, 1)
_register(("सूची", "list"), _builtin_list, 0, 1)
_register(("कुंजियाँ", "keys"), _builtin_keys, 1, 1)
_register(("मान", "values"), _builtin_values, 1, 1)
_register(("समाविष्ट", "has"), _builtin_has, 2, 2)
_register(("हटाओ_कुंजी", "drop"), _builtin_drop, 2, 2)
_register(("तालिका", "dict"), _builtin_dict, 0, 0)
_register(("वर्गमूल", "sqrt"), _builtin_sqrt, 1, 1)
_register(("प्रकार", "type"), _builtin_type, 1, 1)
_register(("गोल", "round"), _builtin_round, 1, 1)
_register(("मिलाओ", "fuse"), _builtin_sorted_join, 1, 1)


class VM:
    """Execute compiled BRAHMA code.

    Parameters
    ----------
    out:
        Callable receiving each printed value (defaults to :func:`print`).
        Pass ``None`` to discard output.
    step_limit:
        Maximum number of executed instructions.  Guards against infinite
        loops in untrusted programs.
    max_depth:
        Maximum call depth.
    globals_:
        Optional pre-populated global namespace.
    """

    def __init__(
        self,
        out: Optional[Callable[[str], None]] = print,
        step_limit: int = DEFAULT_STEP_LIMIT,
        max_depth: int = DEFAULT_MAX_DEPTH,
        globals_: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.out = out
        self.step_limit = step_limit
        self.max_depth = max_depth
        self.globals: Dict[str, Any] = dict(globals_ or {})
        self.frames: List[Frame] = []
        self.steps = 0
        self._source_name = "<input>"
        self._print_builtin = Builtin("दर्शय", self._print_values, 0, None)

    def _print_values(self, *args: Any) -> None:
        if self.out is not None:
            self.out(" ".join(format_value(arg) for arg in args))

    # -- public ----------------------------------------------------------
    def run(self, code: CodeObject) -> Any:
        """Execute ``code`` and return its final value."""
        if not isinstance(code, CodeObject):
            raise TypeError("VM.run expects a CodeObject")
        self._source_name = code.source_name
        main = Frame(code=code, locals=self.globals)
        self.frames = [main]
        self.steps = 0
        while True:
            try:
                return self._execute()
            except RuntimeFault as fault:
                if not self._recover(fault):
                    if fault.source_name is None:
                        fault.source_name = self._source_name
                    if not fault.frames:
                        fault.frames = [
                            (frame.name, frame.last_line) for frame in self.frames
                        ]
                    raise

    def _recover(self, fault: RuntimeFault) -> bool:
        """Unwind to the innermost ``प्रयास`` handler; ``False`` if none.

        Frames are unwound outermost-first: a fault raised three calls deep is
        caught by the nearest enclosing handler, exactly like a real language.
        """
        if not fault.catchable:
            return False
        snapshot = [(frame.name, frame.last_line) for frame in self.frames]
        while self.frames:
            frame = self.frames[-1]
            if frame.handlers:
                target, depth, name = frame.handlers.pop()
                del frame.stack[depth:]
                frame.locals[name] = fault.message
                frame.ip = target
                return True
            self.frames.pop()
        fault.frames = snapshot or fault.frames
        return False

    # -- execution -------------------------------------------------------
    def _execute(self) -> Any:
        frame = self.frames[-1]
        while True:
            frame = self.frames[-1]
            if frame.ip >= len(frame.code.instructions):
                # Falling off the end acts like ``return None``.
                value = None
                if not self._pop_frame(value):
                    return value
                frame = self.frames[-1]
                continue

            instruction = frame.code.instructions[frame.ip]
            frame.last_line = instruction.line
            frame.ip += 1
            self.steps += 1
            if self.steps > self.step_limit:
                raise RuntimeFault(
                    "चरण सीमा (%d) पार हो गई — अनन्त चक्र?" % self.step_limit,
                    line=instruction.line,
                    catchable=False,
                )

            op = instruction.op

            if op == "LOAD_CONST":
                frame.stack.append(instruction.arg)

            elif op == "LOAD_NAME":
                frame.stack.append(self._load_name(frame, instruction))

            elif op == "STORE_NAME":
                frame.locals[instruction.arg] = self._pop(frame, instruction)

            elif op == "POP":
                self._pop(frame, instruction)

            elif op == "DUP":
                if not frame.stack:
                    raise RuntimeFault("स्टैक खाली है (DUP)", line=instruction.line)
                frame.stack.append(frame.stack[-1])

            elif op == "BUILD_LIST":
                count = int(instruction.arg or 0)
                items = [self._pop(frame, instruction) for _ in range(count)]
                items.reverse()
                frame.stack.append(items)

            elif op == "BUILD_DICT":
                count = int(instruction.arg or 0)
                pairs = [self._pop(frame, instruction) for _ in range(count * 2)]
                pairs.reverse()
                mapping = {}
                for position in range(0, len(pairs), 2):
                    key = pairs[position]
                    if isinstance(key, (list, dict)):
                        raise RuntimeFault("कुंजी अपरिवर्तनीय होनी चाहिए", line=instruction.line)
                    mapping[key] = pairs[position + 1]
                frame.stack.append(mapping)

            elif op == "LOAD_SLICE":
                stop = self._pop(frame, instruction)
                start = self._pop(frame, instruction)
                target = self._pop(frame, instruction)
                frame.stack.append(self._slice(target, start, stop, instruction))

            elif op == "LOAD_INDEX":
                index = self._pop(frame, instruction)
                target = self._pop(frame, instruction)
                frame.stack.append(self._index(target, index, instruction))

            elif op == "STORE_INDEX":
                value = self._pop(frame, instruction)
                index = self._pop(frame, instruction)
                target = self._pop(frame, instruction)
                self._store_index(target, index, value, instruction)

            elif op == "BINARY":
                right = self._pop(frame, instruction)
                left = self._pop(frame, instruction)
                frame.stack.append(self._binary(instruction.arg, left, right, instruction))

            elif op == "UNARY":
                operand = self._pop(frame, instruction)
                frame.stack.append(self._unary(instruction.arg, operand, instruction))

            elif op == "COMPARE":
                right = self._pop(frame, instruction)
                left = self._pop(frame, instruction)
                frame.stack.append(self._compare(instruction.arg, left, right, instruction))

            elif op == "JUMP":
                frame.ip = instruction.arg

            elif op == "JUMP_IF_FALSE":
                if not truthy(self._pop(frame, instruction)):
                    frame.ip = instruction.arg

            elif op == "JUMP_IF_TRUE":
                if truthy(self._pop(frame, instruction)):
                    frame.ip = instruction.arg

            elif op == "CALL":
                self._call(frame, instruction)

            elif op == "MAKE_FUNCTION":
                frame.stack.append(
                    Function(instruction.arg, self.globals, [frame.locals] + frame.enclosing)
                )

            elif op == "TRY":
                target, handler_name = instruction.arg
                frame.handlers.append((int(target), len(frame.stack), handler_name))

            elif op == "END_TRY":
                if not frame.handlers:  # pragma: no cover - compiler guarantees this
                    raise RuntimeFault(
                        "'अन्त-प्रयास' का कोई सक्रिय प्रयास नहीं", line=instruction.line
                    )
                frame.handlers.pop()

            elif op == "RETURN":
                value = self._pop(frame, instruction)
                if not self._pop_frame(value):
                    return value
                frame = self.frames[-1]

            elif op == "PRINT":
                value = self._pop(frame, instruction)
                if self.out is not None:
                    self.out(format_value(value))

            elif op == "HALT":
                return None

            elif op == "NOP":
                pass

            else:  # pragma: no cover - validate() should prevent this
                raise RuntimeFault("अज्ञात ऑपकोड %r" % (op,), line=instruction.line)

    # -- stack helpers ---------------------------------------------------
    @staticmethod
    def _pop(frame: Frame, instruction: Instruction) -> Any:
        if not frame.stack:
            raise RuntimeFault("स्टैक अंडरफ़्लो (%s)" % instruction.op, line=instruction.line)
        return frame.stack.pop()

    def _load_name(self, frame: Frame, instruction: Instruction) -> Any:
        name = instruction.arg
        if name in frame.locals:
            return frame.locals[name]
        for scope in frame.enclosing:
            if name in scope:
                return scope[name]
        if name in self.globals:
            return self.globals[name]
        if name in BUILTINS:
            return BUILTINS[name]
        if name in ("दर्शय", "print"):
            return self._print_builtin
        raise RuntimeFault("अपरिभाषित नाम %r" % name, line=instruction.line)

    def _pop_frame(self, value: Any) -> bool:
        self.frames.pop()
        if not self.frames:
            return False
        self.frames[-1].stack.append(value)
        return True

    def _call(self, caller: Frame, instruction: Instruction) -> None:
        argc = int(instruction.arg or 0)
        args = [self._pop(caller, instruction) for _ in range(argc)]
        args.reverse()
        callee = self._pop(caller, instruction)

        if isinstance(callee, Builtin):
            try:
                callee.check_arity(len(args))
                result = callee(*args)
            except RuntimeFault as fault:
                if fault.line is None:
                    fault.line = instruction.line
                raise
            except Exception as exc:  # noqa: BLE001 - surface as a BRAHMA fault
                raise RuntimeFault(
                    "'%s' में त्रुटि: %s" % (callee.name, exc), line=instruction.line
                )
            caller.stack.append(result)
            return

        if not isinstance(callee, Function):
            raise RuntimeFault(
                "%r को आह्वान नहीं किया जा सकता" % (format_value(callee),),
                line=instruction.line,
            )

        code = callee.code
        if len(args) != len(code.params):
            raise RuntimeFault(
                "'%s' को %d आर्ग्युमेंट चाहिए, %d मिले"
                % (code.name, len(code.params), len(args)),
                line=instruction.line,
            )
        if len(self.frames) >= self.max_depth:
            raise RuntimeFault(
                "आह्वान गहराई सीमा पार", line=instruction.line, catchable=False
            )

        local = dict(zip(code.params, args))
        self.frames.append(
            Frame(code=code, locals=local, enclosing=list(callee.closure))
        )

    # -- operators -------------------------------------------------------
    @staticmethod
    def _numeric(op: str, left: Any, right: Any, instruction: Instruction) -> bool:
        numbers = (int, float)
        if isinstance(left, bool) or isinstance(right, bool):
            raise RuntimeFault("ऑपरेटर %r बूलियन पर लागू नहीं" % op, line=instruction.line)
        if not isinstance(left, numbers) or not isinstance(right, numbers):
            raise RuntimeFault(
                "ऑपरेटर %r के लिए संख्या चाहिए, मिला %s और %s"
                % (op, type(left).__name__, type(right).__name__),
                line=instruction.line,
            )
        return True

    def _binary(self, op: str, left: Any, right: Any, instruction: Instruction) -> Any:
        if op == "+":
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            self._numeric(op, left, right, instruction)
            return left + right

        if op in ("-", "*", "/", "%", "**"):
            if op == "*" and isinstance(left, str) and isinstance(right, int) and not isinstance(right, bool):
                return left * right
            self._numeric(op, left, right, instruction)
            if op in ("/", "%") and right == 0:
                raise RuntimeFault("शून्य से भाग दिया गया", line=instruction.line)
            if op == "/":
                return left / right
            if op == "%":
                return left % right
            if op == "**":
                if isinstance(left, int) and isinstance(right, int) and right < 0:
                    return left ** right
                return left ** right
            if op == "-":
                return left - right
            return left * right

        raise RuntimeFault("अज्ञात बाइनरी ऑपरेटर %r" % op, line=instruction.line)  # pragma: no cover

    def _unary(self, op: str, operand: Any, instruction: Instruction) -> Any:
        if op == "not":
            return not truthy(operand)
        if op in ("-", "+"):
            if isinstance(operand, bool) or not isinstance(operand, (int, float)):
                raise RuntimeFault("यूनरी %r के लिए संख्या चाहिए" % op, line=instruction.line)
            return -operand if op == "-" else +operand
        raise RuntimeFault("अज्ञात यूनरी ऑपरेटर %r" % op, line=instruction.line)  # pragma: no cover

    def _compare(self, op: str, left: Any, right: Any, instruction: Instruction) -> bool:
        if op == "==":
            return self._equal(left, right)
        if op == "!=":
            return not self._equal(left, right)
        comparable = (int, float, str)
        if isinstance(left, bool) or isinstance(right, bool):
            raise RuntimeFault("तुलना बूलियन पर लागू नहीं", line=instruction.line)
        if not isinstance(left, comparable) or not isinstance(right, comparable):
            raise RuntimeFault(
                "तुलना के लिए संख्या या शब्द चाहिए, मिला %s और %s"
                % (type(left).__name__, type(right).__name__),
                line=instruction.line,
            )
        if type(left) is not type(right) and not (
            isinstance(left, (int, float)) and isinstance(right, (int, float))
        ):
            raise RuntimeFault(
                "भिन्न प्रकारों की तुलना: %s और %s"
                % (type(left).__name__, type(right).__name__),
                line=instruction.line,
            )
        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right
        raise RuntimeFault("अज्ञात तुलना %r" % op, line=instruction.line)  # pragma: no cover

    @staticmethod
    def _equal(left: Any, right: Any) -> bool:
        if isinstance(left, bool) != isinstance(right, bool):
            return False
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left == right
        if type(left) is not type(right):
            return False
        return left == right

    @staticmethod
    def _slice(target: Any, start: Any, stop: Any, instruction: Instruction) -> Any:
        if not isinstance(target, (str, list)):
            raise RuntimeFault("काट केवल शब्द/सूची पर लागू है", line=instruction.line)
        for bound, name in ((start, "आरम्भ"), (stop, "अन्त")):
            if bound is None:
                continue
            if isinstance(bound, bool) or not isinstance(bound, int):
                raise RuntimeFault("काट का %s पूर्णांक होना चाहिए" % name, line=instruction.line)
        return target[start:stop]

    @staticmethod
    def _index(target: Any, index: Any, instruction: Instruction) -> Any:
        if isinstance(target, dict):
            if index not in target:
                raise RuntimeFault("कुंजी नहीं मिली: %r" % (index,), line=instruction.line)
            return target[index]
        if not isinstance(target, (str, list)):
            raise RuntimeFault("केवल शब्द/सूची/तालिका का सूचकांक लिया जा सकता है", line=instruction.line)
        if isinstance(index, bool) or not isinstance(index, int):
            raise RuntimeFault("सूचकांक पूर्णांक होना चाहिए", line=instruction.line)
        length = len(target)
        real = index + length if index < 0 else index
        if real < 0 or real >= length:
            raise RuntimeFault(
                "सूचकांक %d सीमा से बाहर (लम्बाई %d)" % (index, length), line=instruction.line
            )
        return target[real]

    @staticmethod
    def _store_index(target: Any, index: Any, value: Any, instruction: Instruction) -> None:
        if isinstance(target, dict):
            if isinstance(index, (list, dict)):
                raise RuntimeFault("कुंजी अपरिवर्तनीय होनी चाहिए", line=instruction.line)
            target[index] = value
            return
        if not isinstance(target, list):
            raise RuntimeFault("केवल सूची/तालिका में मान लिखा जा सकता है", line=instruction.line)
        if isinstance(index, bool) or not isinstance(index, int):
            raise RuntimeFault("सूचकांक पूर्णांक होना चाहिए", line=instruction.line)
        length = len(target)
        real = index + length if index < 0 else index
        if real < 0 or real >= length:
            raise RuntimeFault(
                "सूचकांक %d सीमा से बाहर (लम्बाई %d)" % (index, length), line=instruction.line
            )
        target[real] = value


def run_code(code: CodeObject, out: Optional[Callable[[str], None]] = print, **kwargs: Any) -> Any:
    """Convenience helper: execute ``code`` on a fresh :class:`VM`."""
    return VM(out=out, **kwargs).run(code)
