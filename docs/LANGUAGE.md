# BRAHMA भाषा संदर्भ (Language Reference)

Version 3.2.0 — implemented by `brahma/` (lexer → parser → compiler → VM).
Grammar history: 3.0.0 added dicts, slices and multi-line literals; 3.1.0 added
closures, `प्रयास`/`पकड़` exception handling and `$"…{expr}…"` interpolation;
3.2.0 added `उठाओ` (raise), `अन्ततः` (finally) and slice assignment.

BRAHMA is a small, dynamically typed language whose native vocabulary is
Sanskrit. Every keyword is available in Devanagari **and** in ASCII, so the
same program can be written either way:

```brahma
यदि अ > 3
    दर्शय "बड़ा"
अन्त
```
```brahma
if a > 3
    print "big"
end
```

---

## 1. Lexical structure

### 1.1 Identifiers

An identifier starts with a Unicode letter or `_` and continues with letters,
combining marks, digits or `_`. Devanagari conjuncts therefore work naturally:

```brahma
स्थापय कर्म_संख्या = ७
दर्शय कर्म_संख्या          # 7
```

### 1.2 Numbers

* integers: `42`, `१०` (Devanagari digits are normalised)
* floats: `3.5`, `1e3`, `२.५`
* numerals may mix scripts in one literal (`१2३` → `123`)

There is no separate integer/float arithmetic rule: `/` always yields a float,
so `20 / 10` prints `2.0`.

### 1.3 Strings

Single or double quoted, UTF-8, with escapes `\n \t \r \\ \" \' \0 \uXXXX`.
Strings are immutable sequences; `लम्बाई()` gives their length in code points.

A string prefixed with `$` is **interpolated**: every `{…}` inside it is a
full expression, converted with `पाठ()` and joined with `+`.

```brahma
नाम = "ब्रह्म"
दर्शय $"नमस्ते {नाम}! 2 + 3 = {2 + 3}"
दर्शय $"ब्रेस {{लिटरल}}"          # literal braces: {{ and }}
```

A plain string (`"…"`, no `$`) is never interpolated, so JSON literals such as
`"{\"ok\": true}"` keep their braces.  An unclosed `{`, a stray `}`, an empty
`{}` or an invalid embedded expression is a **parse error** with a line number.

### 1.4 Comments

From `#` to end of line.

### 1.5 Statements and newlines

Statements are newline terminated. `;` is accepted as an additional separator,
so `अ = 1; ब = 2` is two statements. Blank lines are ignored.

---

A newline ends a statement, **except inside `( … )`, `[ … ]` or `{ … }`**, where
it is a continuation. Multi-line table literals, list literals and call
arguments are therefore ordinary code:

```brahma
स्थापय त = {
    "नाम": "सूत्र-OS",
    "संस्करण": 3
}
```

---

## 2. Keywords

| Sanskrit | ASCII | Meaning |
|---|---|---|
| `स्थापय` | `let` | declare / assign |
| `दर्शय` | `print` | print a value |
| `यदि` | `if` | conditional |
| `अन्यथायदि` | `elif` | else-if |
| `अन्यथा` | `else` | else |
| `अन्त` | `end` | close a block |
| `यावत्` | `while` | loop |
| `विराम` | `break` | leave loop |
| `चल` | `continue` | next iteration |
| `कार्य` | `func` / `def` | define function |
| `प्रयास` | `try` | guarded block |
| `पकड़` | `catch` | bind the fault and handle it |
| `अन्ततः` | `finally` | always run, however the block is left |
| `उठाओ` | `raise` | raise a fault with a message |
| `प्रत्यागमन` | `return` | return from function |
| `सत्य` | `true` | boolean true |
| `असत्य` | `false` | boolean false |
| `शून्य` | `null` / `none` | null value |
| `च` | `and` | logical and (short-circuit) |
| `वा` | `or` | logical or (short-circuit) |
| `न` | `not` | logical negation |

Blocks are **terminated by `अन्त`**, not indented. Indentation is cosmetic.

---

## 3. Values and types

| Type | Examples | Truthiness |
|---|---|---|
| number (int) | `0`, `42`, `-7` | false when `0` |
| number (float) | `3.5`, `2.0` | false when `0.0` |
| string | `"नमस्ते"`, `""` | false when empty |
| boolean | `सत्य`, `असत्य` | as-is |
| list | `[1, 2, 3]` | false when empty |
| table (dict) | `{"क": 1}` | false when empty |
| null | `शून्य` | always false |

Equality is **type-strict** for booleans: `सत्य == 1` is `असत्य`. Integers and
floats compare numerically: `1 == 1.0` is `सत्य`.

---

## 4. Expressions

### 4.1 Operators, from loosest to tightest

| Level | Operators | Associativity |
|---|---|---|
| 1 | `वा` / `or` | left |
| 2 | `च` / `and` | left |
| 3 | `==` `!=` | left |
| 4 | `<` `<=` `>` `>=` | left |
| 5 | `+` `-` | left |
| 6 | `*` `/` `%` | left |
| 7 | `न`/`not`, unary `-`, unary `+` | right |
| 8 | `**` | right |
| 9 | `f(args)`, `x[i]`, `x[a:b]` | left |
| 10 | literals, names, `( … )`, `[…]`, `{…}` | — |

`-2 ** 2` is `-4` (power binds tighter than unary minus), `2 ** 3 ** 2` is `512`.

### 4.2 Semantics

* `+` concatenates strings and lists; otherwise numeric.
* `*` repeats a string by an integer count; otherwise numeric.
* `/` is true division (always float); `%` follows Python sign rules
  (`-7 % 3 == 2`).
* `च`/`and` and `वा`/`or` short-circuit and **return an operand** (like Python):
  `0 च 5` → `0`, `2 च 5` → `5`.
* Mixing types in arithmetic or ordered comparison is a runtime error with a
  precise diagnostic — there is no silent coercion.
* `x[a:b]` slices a string or a list; either bound may be omitted (`x[:3]`,
  `x[2:]`), negative bounds count from the end, and a non-integer bound is a
  runtime error.
* `{कुंजी: मान, …}` builds a table. Keys must be immutable (string, number,
  boolean, `शून्य`); a missing key on read is a runtime error naming the key,
  and assigning `त["नयी"] = मान` inserts it.

### 4.3 Assignment

```brahma
अ = 1                    # simple
अ += 2                   # compound: += -= *= /= %=
स[0] = 9                 # list element
त["नाम"] = "ब्रह्म"      # table entry (inserts when missing)
ग[1][0] = 30             # nested element (chains of `[…]` on the left)
स्थापय ख = 3             # explicit declaration (informational)
```

Inside a function, assignment always creates/updates a **local** variable.
Functions may read globals but cannot rebind them (there is no `global`).

---

## 5. Statements

```brahma
# print
दर्शय "नमस्ते"

# condition
यदि अ > 10
    दर्शय "बड़ा"
अन्यथायदि अ > 5
    दर्शय "मध्यम"
अन्यथा
    दर्शय "छोटा"
अन्त

# loop
स्थापय i = 0
यावत् i < 5
    यदि i == 3
        विराम
    अन्त
    दर्शय i
    i += 1
अन्त

# function
कार्य योग(क, ख)
    प्रत्यागमन क + ख
अन्त
दर्शय योग(2, 3)

# guarded block, with cleanup
प्रयास
    दर्शय 10 / 0
पकड़ त्रुटि
    दर्शय "विफल: " + त्रुटि
अन्ततः
    दर्शय "सफाई"
अन्त

# raise your own fault
प्रयास
    यदि 10 < 0
        उठाओ "ऋणात्मक"
    अन्त
पकड़ त
    दर्शय त
अन्त

# slice assignment
स = [1, 2, 3, 4]
स[1:3] = [9, 9, 9]        # [1, 9, 9, 9, 4]
स[0:0] = [0]              # insert at the front
स[-1:] = []               # delete the tail

# closure: the inner function captures `n`
कार्य वृद्धि(n)
    कार्य जोड़(x)
        प्रत्यागमन x + n
    अन्त
    प्रत्यागमन जोड़
अन्त
जोड़ो = वृद्धि(10)
दर्शय जोड़ो(5)          # 15
```

* `प्रत्यागमन` without a value returns `शून्य`.
* Falling off the end of a function returns `शून्य`.
* `विराम`/`चल` outside a loop is a **parse error** (caught before execution).
* `प्रत्यागमन` outside a function is a parse error.
* `उठाओ expr` raises a fault carrying `पाठ(expr)`.  `उठाओ` with no value uses
  a default message.  A fault with no handler stops the program with a
  traceback, exactly like a failed division.
* `अन्ततः` runs on **every** exit from the guard — normal completion, a caught
  fault, an uncaught fault (which then keeps propagating), and every
  `प्रत्यागमन`/`विराम`/`चल` inside it.  `प्रयास` requires at least one of
  `पकड़`/`अन्ततः`.
* `x[a:b] = सूची` replaces that slice; the replacement may be longer or
  shorter, so it also inserts (`a == b`) and deletes (`[]`).  Only lists are
  assignable — strings are immutable.
* `प्रयास … पकड़ नाम … अन्त`: a fault raised anywhere inside the block — including
  inside functions it calls — unwinds to the nearest handler, which receives the
  message in `नाम` as a string; execution then continues after `अन्त`.  Nested
  blocks bind innermost-first.  The step-budget and call-depth guards are
  **not** catchable, so a runaway loop cannot be swallowed.
* `कार्य` bodies are lexically scoped: names are looked up in the current frame,
  then in each enclosing scope captured at definition time, then in globals.
  Two closures made by two calls are independent.

---

## 6. Builtin functions

| Sanskrit | ASCII | Arity | Behaviour |
|---|---|---|---|
| `दर्शय` | `print` | 0+ | prints (also a statement keyword) |
| `लम्बाई` | `len` | 1 | length of string/list |
| `संख्या` | `int` | 1 | parse/convert to integer |
| `दशमलव` | `float` | 1 | convert to float |
| `पाठ` | `str` | 1 | render a value as text |
| `सत्यता` | `bool` | 1 | truthiness as boolean |
| `निरपेक्ष` | `abs` | 1 | absolute value |
| `न्यूनतम` | `min` | 1+ | minimum of values or of a list |
| `अधिकतम` | `max` | 1+ | maximum of values or of a list |
| `श्रेणी` | `range` | 1–3 | list of integers |
| `जोड़ो` | `join` | 2 | join a list with a separator |
| `जोड़ें` | `append` | 2 | append to a list, returns the list |
| `विभाजन` | `split` | 1–2 | split a string (default: whitespace) |
| `प्रतिस्थापन` | `replace` | 3 | replace every occurrence |
| `त्रिम` | `trim`/`strip` | 1 | strip surrounding whitespace |
| `बड़े` / `छोटे` | `upper`/`lower` | 1 | case conversion |
| `खोज` | `find` | 2 | index of a substring, `-1` if absent |
| `दोहराओ` | `repeat` | 2 | repeat a string *n* times |
| `क्रम` | `sort` | 1 | new sorted list |
| `उलटा` | `reverse` | 1 | new reversed list |
| `हटाओ` | `pop` | 1–2 | remove and return an element |
| `सम्मिलित` | `insert` | 3 | insert at an index, returns the list |
| `विस्तार` | `extend` | 2 | append another list's items |
| `गिनती` | `count` | 2 | occurrences of a value |
| `स्थान` | `index_of` | 2 | index of a value (error if absent) |
| `योगफल` | `sum` | 1 | sum of numbers |
| `सूची` | `list` | 0–1 | new list from a list/string/table |
| `कुंजियाँ` | `keys` | 1 | table keys |
| `मान` | `values` | 1 | table values |
| `समाविष्ट` | `has` | 2 | key membership |
| `हटाओ_कुंजी` | `drop` | 2 | remove a key, returns its value |
| `तालिका` | `dict` | 0 | new empty table |
| `वर्गमूल` | `sqrt` | 1 | square root (errors on negatives) |
| `प्रकार` | `type` | 1 | type name in Sanskrit |
| `गोल` | `round` | 1 | nearest integer |
| `मिलाओ` | `fuse` | 1 | concatenate rendered list items |

Builtins check their argument count and raise a BRAHMA error (not a Python
`TypeError`) on misuse.

---

## 7. Errors and diagnostics

Three phases, each with its own error type and source position:

* `LexError` / `ParseError` / `CompileError` — before execution.
* `RuntimeFault` — during execution, with a call-stack trace (or caught by
  `प्रयास`/`पकड़`, which converts it into a string in the handler variable).

```
demo.sutra:4:5: अपरिभाषित नाम 'अ'
आह्वान शृंखला:
  <module> में (पंक्ति 6)
  f में (पंक्ति 4)
```

Runtime guards:

* step budget (default 1,000,000 instructions) — detects infinite loops;
* call-depth limit (default 500);
* index/type/arity checks on every operation.

The step budget makes accidental hangs impossible, but it is **not** a security
sandbox: BRAHMA programs cannot touch the filesystem or network at all, because
no such builtins exist in 3.2.0.

---

## 8. Bytecode and the `.sbc` container

Compilation produces a `CodeObject` tree. Serialised form:

```
SUTRA1\n
{
  "format": "brahma-bytecode",
  "version": 1,
  "entry": {
    "name": "<module>",
    "params": [],
    "source": "prog.sutra",
    "instructions": [
      {"op": "LOAD_CONST", "arg": 1, "line": 1},
      {"op": "PRINT", "line": 1},
      {"op": "HALT", "line": 1}
    ]
  }
}
```

The JSON container is deliberate: portable across Python versions, diffable,
inspectable with `brahma disasm`. Loading validates the format name, the
version, every opcode, every jump target and function object; malformed images
raise `BytecodeError` and never execute partially.

### 8.1 Opcodes

| Opcode | Argument | Effect |
|---|---|---|
| `NOP` | — | no operation |
| `LOAD_CONST` | value | push constant |
| `LOAD_NAME` | name | push local → global → builtin (else error) |
| `STORE_NAME` | name | pop into local |
| `POP` | — | drop top of stack |
| `DUP` | — | duplicate top |
| `BUILD_LIST` | n | pop *n* values into a list |
| `LOAD_INDEX` | — | `target idx` → element |
| `STORE_INDEX` | — | `target idx value` → store |
| `BINARY` | `+ - * / % **` | pop 2, push result |
| `UNARY` | `- + not` | pop 1, push result |
| `COMPARE` | `== != < <= > >=` | pop 2, push boolean |
| `JUMP` | target | set instruction pointer |
| `JUMP_IF_FALSE` | target | pop, jump when falsy |
| `JUMP_IF_TRUE` | target | pop, jump when truthy |
| `CALL` | argc | call function/builtin |
| `RETURN` | — | return from frame |
| `MAKE_FUNCTION` | code object | push function value (captures the frame) |
| `TRY` | `[handler, name]` | push a handler: `(ip, stack depth, name)` |
| `END_TRY` | — | pop the innermost handler (normal completion) |
| `RAISE` | — | pop a message, raise a runtime fault |
| `RERAISE` | — | re-raise the fault this frame is handling |
| `STORE_SLICE` | — | `target start stop value` → replace a list slice |
| `PRINT` | — | pop and print |
| `HALT` | — | stop the program |

---

## 9. CLI

```bash
python -m brahma run      prog.sutra          # execute
python -m brahma check    prog.sutra          # compile only (fast CI gate)
python -m brahma compile  prog.sutra -o p.sbc # to bytecode
python -m brahma disasm   prog.sutra|p.sbc    # bytecode listing
python -m brahma run-bytecode p.sbc           # execute bytecode
python -m brahma repl                         # interactive (multi-line blocks)
python -m brahma version
```

Exit codes: `0` success, `1` program/IO error, `2` usage error.

After `pip install brahma-lang`, the same commands are available as `brahma`.

---

## 10. Known limitations (3.2.0)

Honest list — these are not implemented:

* no user-defined classes/objects, no tuples or sets
* no `import` / module system: a program is a single file
* closures are **read-only**: assigning to a captured name creates a local in
  the inner function (there is no `nonlocal`/`global` declaration)
* no exception *types*: every fault is a message string, so `पकड़` cannot
  discriminate between, say, arithmetic and lookup errors
* no `nonlocal`/`global`, so a closure cannot reassign a captured name
* no tail-call optimisation, no JIT; the VM is a straightforward interpreter
* the C VM in `native_vm/` is a **separate**, much smaller prototype and does
  not implement this specification (it has no `TRY`/`MAKE_FUNCTION` closure
  support)

The grammar accepted by `brahma/parser.py` is the authoritative one; this
document describes the same language.
