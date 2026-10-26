# BRAHMA भाषा संदर्भ (Language Reference)

Version 2.1.0 (grammar unchanged since 1.2.0) — implemented by `brahma/` (lexer → parser → compiler → VM).

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

### 1.4 Comments

From `#` to end of line.

### 1.5 Statements and newlines

Statements are newline terminated. `;` is accepted as an additional separator,
so `अ = 1; ब = 2` is two statements. Blank lines are ignored.

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
| 9 | `f(args)`, `x[i]` | left |
| 10 | literals, names, `( … )`, `[…]` | — |

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

### 4.3 Assignment

```brahma
अ = 1            # simple
अ += 2           # compound: += -= *= /= %=
स[0] = 9         # list element
स्थापय ख = 3     # explicit declaration (informational)
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
```

* `प्रत्यागमन` without a value returns `शून्य`.
* Falling off the end of a function returns `शून्य`.
* `विराम`/`चल` outside a loop is a **parse error** (caught before execution).
* `प्रत्यागमन` outside a function is a parse error.

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

Builtins check their argument count and raise a BRAHMA error (not a Python
`TypeError`) on misuse.

---

## 7. Errors and diagnostics

Three phases, each with its own error type and source position:

* `LexError` / `ParseError` / `CompileError` — before execution.
* `RuntimeFault` — during execution, with a call-stack trace.

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
no such builtins exist in 2.1.0.

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
| `MAKE_FUNCTION` | code object | push function value |
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

## 10. Known limitations (2.1.0)

Honest list — these are not implemented:

* no user-defined classes/objects, no dictionaries, no tuples or sets
* no `import` / module system: a program is a single file
* no string interpolation or formatting functions
* no language-level exceptions (`try`/`catch`)
* no slicing (`x[1:3]`), only single indexing
* no closures; functions see globals read-only
* no tail-call optimisation, no JIT; the VM is a straightforward interpreter
* the C VM in `native_vm/` is a **separate**, much smaller prototype and does
  not implement this specification
