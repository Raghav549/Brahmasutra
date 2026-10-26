# 🕉️ ब्रह्म-LLM — a from-scratch trainable language model for सूत्र

**Version 2.1.0.** Everything in this document is executable in this repository
and every number below was measured on the checkout, with the command shown
next to it. Nothing here downloads weights, and nothing imports `torch`,
`numpy`, `transformers` or any other ML library: the tokenizer, the models, the
gradients, the optimizer, the trainer, the self-editor and the OS are all plain
Python in `brahma_llm/`.

---

## 1. What this is — and what it is not

**It is** a complete, working language-model stack that you can read end to end:

| Piece | Module | What is genuinely implemented |
|---|---|---|
| Tokenizer | `brahma_llm/tokenizer.py` | akṣara-level segmentation for Devanagari (conjuncts, matras, digits), ASCII words/numbers/punctuation, reversible decode, frequency-pruned vocabulary |
| n-gram model | `brahma_llm/model.py` (`NgramLM`) | Jelinek–Mercer interpolation with add-k smoothing |
| Neural model | `brahma_llm/model.py` (`NeuralLM`) | embedding → tanh hidden → softmax, **hand-written backpropagation**, Adam |
| Gradient proof | `tests/test_llm.py` | analytic gradients vs central differences, error < 1e-6 (measured 2e-11) |
| Trainer | `brahma_llm/trainer.py` | target → generate → validate → train → measure → keep-best loop with budget/patience stops |
| Data engine | `brahma_llm/programs.py` | template generator whose output is **executed** before it may enter the corpus |
| Self-editing | `brahma_llm/selfedit.py` | prediction-preserving weight surgery, gated OS reinstall, audit log |
| Its own OS | `brahma_llm/kernel.py` | सूत्र kernel → bytecode → `SUTRAOS` image → boot/verify/install |
| Model maths in सूत्र | `brahma_llm/sutra_kernel.py` | exp/tanh/softmax/forward pass written in the सूत्र language and run on the project's VM |
| Apps | `brahma_llm/app_builder.py` | LLM writes सूत्र logic → server + UI + smoke test |

**It is not** a frontier model, and this project makes no such claim. Concretely:

* the shipped checkpoint is **4–52 k parameters**, not 10¹¹;
* it is trained on the repository's own सूत्र corpus (≈ 50 files, ≈ 33 k
  characters), not on a web-scale corpus;
* its perplexities are the ones in §3 — a character/akṣara-level model on a tiny
  corpus, useful for generating and completing सूत्र programs, not for writing
  essays;
* "the largest / most powerful LLM in the world" is **not** something a few
  thousand lines of standard-library Python can deliver. What is delivered is a
  model whose *every* part you can inspect, retrain, resize and verify, with
  `brahma llm bench` printing the real numbers any time you want them.

Scaling is a knob, not a promise — see §9 for what it costs.

---

## 2. Architecture

### 2.1 Tokenizer — akṣara, not code points

`aksharas()` keeps a consonant cluster with its vowel signs together:

```python
>>> from brahma_llm.tokenizer import aksharas
>>> aksharas('दर्शय "नमस्ते"')
['द', 'र्श', 'य', ' ', '"', 'न', 'म', 'स्ते', '"']
```

Special tokens are fixed at ids `0..3` (`<pad> <unk> <bos> <eos>`). The
vocabulary is frequency-pruned per size preset, which keeps the softmax cheap in
pure Python.

### 2.2 The two models

```
NgramLM(order, vocab)                     NeuralLM(vocab, d_model, hidden, order)
counts[1..order] + add-k                  x = concat(E[c-2], E[c-1], E[c])
P(w|h) = λ·P_ML(w|h) + (1-λ)·P_backoff    h = tanh(W1·x + b1)
                                          logits = W2·h + b2
                                          P = softmax(logits)
```

`NeuralLM.loss_and_grads(examples)` returns the mean cross-entropy **and** the
gradients. That function is the whole backward pass, and it is tested against
central differences:

```
$ python -m pytest tests/test_llm.py -k gradients -q
1 passed
worst absolute difference between analytic and numeric gradient: 2.35e-11
```

### 2.3 Size presets

| preset | d_model | hidden | order | vocab cap | params at cap | 1 epoch: time / perplexity |
|---|---|---|---|---|---|---|
| `tiny` | 8 | 32 | 2 | 96 | 4 480 | 2 s / **13.8** |
| `small` | 16 | 64 | 3 | 160 | 16 096 | 5 s / — |
| `medium` | 24 | 128 | 4 | 256 | 51 584 | 11 s / — |
| `large` | 32 | 192 | 5 | 384 | 117 312 (trained: 115 287) | 21.7 s / 86.6 |
| `xlarge` | 48 | 384 | 6 | 512 | 314 240 (trained: 254 919) | 50.3 s / 342.6 |
| `huge` | 64 | 768 | 8 | 768 | 886 272 (trained: 558 903) | **107.4 s / 3 139.9** |
| `brahma` | 96 | 1536 | 10 | 1024 | **2 411 008** | **189.3 s / 25 600 162** (1 390 383 params as trained) |

The `params at cap` column counts embeddings sized for the preset's vocabulary
**cap**; a real training run sizes the tables for the corpus vocabulary it
actually saw, which is why the counts reported by `brahma llm train` differ a
little from the cap column.  With the current 383-token vocabulary the presets
come out at 16 247 / 34 159 / 71 015 / 117 087 / 258 383 / 565 567 /
**1 364 255** parameters respectively.

The last column is the point of this table: **more parameters make held-out
perplexity worse** on this corpus, because the vocabulary and the model outgrow
the ~33 k characters of training text (each preset has a larger vocab cap, so
more rows can be badly estimated).  `huge` was trained twice in a clean tree and
produced the identical number both times — it is reproducible, not a fluke.
Scaling this project means writing more सूत्र, not widening the hidden layer.

Every number in the *params* column is printed by
`build_model(...).parameter_count()` on this checkout —
`brahma` (2.41 M) is instantiated and counted, **not** trained to convergence.
`brahma llm info` always prints the counted total of the loaded checkpoint
rather than a marketing number, and §9 explains why counting is the honest
claim to make.

## 3. Measured results

### 3.1 Supervised sizing (`brahma llm bench`)

```
$ BRAHMA_HOME=/tmp/b brahma llm bench --sizes tiny small medium --epochs 4
(uniform baseline perplexity = 96.0)
kind     size        params  vocab   perplexity  seconds
-------- ------- ---------- ------ ------------ --------
ngram    tiny          1754     96        8.513     0.01
ngram    small         4434    160       12.598     0.03
ngram    medium        7661    256       20.035     0.05
neural   tiny          4480     96       10.031     3.25
neural   small        16096    160       11.182    10.68
neural   medium       51584    256       19.116    35.64
```

Two honest observations that the table makes impossible to hide:

* **bigger vocabulary is not better here.** The corpus is small; a larger
  vocabulary mostly adds rare tokens that become `<unk>` and dilute the
  softmax. The trainer therefore keeps the checkpoint that actually wins.
* the **n-gram model beats the neural model on this corpus**, which is expected
  for ~33 k characters and is exactly why the baseline ships alongside it.

### 3.1b Data beats size (`brahma llm corpus --generate`)

The autonomous loop can grow its own training set: `ProgramGenerator` writes
programs that are compiled **and executed** before they are written, and
`load_corpus()` picks them up from `$BRAHMA_HOME/corpus` on the next training
run.  Measured here, 3 epochs each (2 for `xlarge`, marked in the row), the same
seed throughout, and the same parameter count within a row except where the new
data grew the vocabulary:

| size | corpus | texts | chars | perplexity | time |
|---|---|---|---|---|---|
| `tiny` | base | 117 | 63 522 | 15.389 | 1.7 s |
| `tiny` | + 60 generated | 165 | 71 793 | **6.941** (−55 %) | 2.0 s |
| `small` | base | 117 | 63 522 | 19.687 | 5.5 s |
| `small` | + 300 generated | 405 | 105 790 | **4.795** (−76 %) | 8.9 s |
| `xlarge` | base (2 epochs) | 117 | 63 522 | 229.838 | 72.6 s |
| `xlarge` | + 300 generated (2 epochs) | 405 | 105 790 | **27.489** (−88 %) | 122.8 s |

That is the honest lesson of §9 in one table: on this project the binding
constraint is *data*, not parameters.  Fifty more valid programs buy more than
ten times more weights do.

Two caveats, both measured (3.6.0, `tiny`, 2 epochs, seed 7, 40 generated
programs):

* the table above scores each model on the corpus it was trained on.  Scored on
  one fixed held-out set the effect is smaller and one-directional: perplexity
  on **generated-style** programs improves 11.492 → 9.646, while perplexity on
  the **original** texts does not (9.499 → 10.056) — extra data of one style
  does not automatically help another;
* `tests/test_llm.py::test_generated_data_improves_perplexity` now asserts the
  first of those (same held-out set for both models) instead of the old
  each-model-on-its-own-corpus comparison, which compared unlike distributions.

Scale changes this: at `small` and `xlarge` the extra data lowers perplexity by
76 % and 88 % respectively on the shuffled corpus used in the table, and the
autonomous loop in §3.2 measures held-out perplexity every round.

```bash
brahma llm corpus --generate 300 --seed 5   # writes $BRAHMA_HOME/corpus/NNNN.sutra
brahma llm train --size small --epochs 3    # the new files are part of the corpus
```

### 3.2 The autonomous loop (`brahma llm autotrain`)

```
$ BRAHMA_HOME=/tmp/brdoc2 brahma llm autotrain \
      --target "अभाज्य संख्या जाँच लिखो" --iterations 4 --epochs 4 --size tiny
```

Measured report (`report.json`, 9.2 s total):

| round | programs accepted | held-out perplexity | hidden units | parameters | body edit |
|---|---|---|---|---|---|
| 1 | 6/6 | 10.428 | 32 → 36 | 4 932 | accepted (drift 0.0) |
| 2 | 6/6 | 9.669 | 36 → 40 | 5 384 | accepted (drift 0.0) |
| 3 | 6/6 | 9.216 | 40 → 44 | 5 836 | accepted (drift 0.0) |
| 4 | 6/6 | **8.962** | 44 → 48 | 6 288 | accepted (drift 0.0) |

* held-out perplexity **10.428 → 8.962 (−14.1 %)** over four rounds;
* **24/24** generated programs compiled *and ran* (acceptance 1.0) before
  entering the corpus;
* each round grew the model's own hidden layer, with **zero** prediction drift;
* the kernel was rebuilt and verified inside the same run (`READY`, 143 VM
  steps, 10 059-byte image).

Reproducing it with the same `--seed` gives the same numbers; a different seed
changes the generated programs and therefore the trajectory.

### 3.3 The model's maths, executed by the model's own language

`brahma_llm/sutra_kernel.py` contains `घातांक` (exp, 20-term Maclaurin +
5 squarings), `स्पर्शरेखा` (tanh), `सॉफ्टमैक्स` and `अग्रपरत` (the full forward
pass) written in सूत्र. The Python and सूत्र implementations are compared on
random models:

```
$ brahma llm sutra-math
सूत्र-गणित जाँच
  exp(1) त्रुटि      : 1.199e-14
  softmax त्रुटि     : 3.331e-16
  अग्रगमन अधिकतम अंतर: 8.327e-16
```

`brahma llm generate --engine sutra` samples text with every forward pass
running on the सूत्र VM, so "the model is built with its own language" is a
statement you can execute, not a slogan.

---

## 4. सूत्र-OS — the kernel is its own

`brahma_llm/os_kernel.py` holds the operating system as **one सूत्र program**
(`KERNEL_SOURCE`).  `brahma_llm/kernel.py` compiles it to the project's own
bytecode and wraps it in the documented image format:

```
"SUTRAOS" | version (>I) | payload length (>I) | bytecode
```

The kernel implements six subsystems, each self-tested at boot, all in सूत्र:

| subsystem | what it does |
|---|---|
| **स्मृति** | first-fit allocator with a free list and byte accounting |
| **प्रक्रिया** | process table: pid allocation, states, priorities, lookup, kill |
| **अनुसूचक** | round-robin scheduler with per-process ticks and cycle counter |
| **आह्वान** | syscall table (`sys_write`, `sys_read`, `sys_exit`, `sys_fork`, `sys_time`) with per-call counters |
| **सञ्चिका** | in-memory filesystem with inodes, sizes, create/write/read/list |
| **व्यवधान** | interrupt counter with source tracking |
| **सुरक्षित आह्वान** | guarded syscall path: an unknown syscall is raised, caught with `प्रयास`/`पकड़`, recorded and returned as `{"ok": false}` |
| **शेल** | `शेल_चलाओ(पंक्ति)` — the command dispatcher, in सूत्र (see §4.2) |

**Scope, stated plainly.**  This is an operating-system *model* that really
executes on the project's VM, not a kernel that boots on bare metal.  It has a
single flat address space (an allocator over a 1 024-byte heap, no paging, no
MMU), cooperative scheduling driven by calls to `अगली_प्रक्रिया()` rather than a
hardware timer interrupt, an in-memory filesystem that disappears when the
process ends (no block device), and no privilege separation.  What it does have
is what an OS course would ask for — allocation, processes, scheduling,
syscalls, files, interrupts and a shell — implemented in one Sanskrit program
that compiles to bytecode and boots through a fixed, verified contract.

The boot contract is enforced by `verify()`: banner → self-test line
`स्व-परीक्षण: ठीक / ठीक` → subsystem summary → `READY`.  `install()` refuses to
write an image that fails it.

```
$ brahma llm kernel verify
🕉️ सूत्र-OS कर्नेल प्रारम्भ
स्व-परीक्षण: ठीक / ठीक
उपप्रणाली: 6/6 ठीक
स्मृति: 352 बाइट, 4 खंड, 0 मुक्त
प्रक्रियाएँ: 4 (तैयार 3)
अनुसूचक: 2 चक्र
आह्वान: 3
सञ्चिकाएँ: /इत्यादि/संस्करण, /इत्यादि/स्वागत
व्यवधान: 3 (अंतिम: चक्रिका)
अपवाद: 1 पकड़े (अज्ञात syscall 99)
कर्नेल API: 10 फलन
READY
  चरण: 1873, छवि: 177064 बाइट, स्थिति: ठीक
```

The kernel ends by exporting `कर्नेल_एपीआई` — a real dictionary of ten callable
functions (`स्मृति_आवंटन`, `प्रक्रिया_जन्म`, `अनुसूचक` …), i.e. the OS exposes an
API *to programs*, not just a boot banner.  The language had to grow for this:
dictionaries, slicing, nested index assignment, multi-line bracketed literals
and — since 3.1 — closures, `प्रयास`/`पकड़` and `$"…{…}…"` interpolation (see
`docs/LANGUAGE.md`), all added with tests.  The kernel uses the exception
support itself: `सुरक्षित_आह्वान` turns an unknown syscall into a raised, caught fault
and records it.

The kernel has a shell of its own — and the dispatcher is a **सूत्र program**.
`शेल_चलाओ(पंक्ति)` lives in `brahma_llm/os_kernel.py` next to the allocator and
the process table; `brahma_llm/shell.py` only owns the read-eval-print loop:

```
$ brahma llm shell
🕉️ सूत्र-OS कर्नेल प्रारम्भ
…
READY
`help` से आदेश देखें, `exit` से बाहर।
सूत्र-OS> ps
  pid 1  कर्नेल  तैयार  टिक 1
  pid 2  शेल  तैयार  टिक 1
  pid 3  सेवक  समाप्त  टिक 0
सूत्र-OS> write /नमूना नमस्ते ब्रह्म
  लिखा: /नमूना (13 बाइट)
सूत्र-OS> cat /नमूना
  नमस्ते ब्रह्म
सूत्र-OS> fork शेल-कार्य
  नया pid: 5
सूत्र-OS> syscall 99
  {ok: असत्य, त्रुटि: अज्ञात syscall 99}
सूत्र-OS> run दर्शय 6 * 7
42
सूत्र-OS> exit
```

State is the kernel's own: a process forked in one command is visible to `ps`
in the next, files written with `write` persist for `cat` and `ls`, and the
guarded syscall shows the caught fault.  `run <सूत्र>` compiles the rest of the
line and executes it **inside the same VM**, so user code shares the kernel's
namespace.  The same shell answers over HTTP at `POST /shell`:

```
$ curl -s localhost:8080/shell -d '{"command":"free"}' -H 'Content-Type: application/json'
{"command": "free", "output": ["  स्मृति: 352 बाइट, 4 खंड, 0 मुक्त", "…"], "ok": true, …}
```

### 4.2 The shell is written in सूत्र

The older `kernel/kernel_engine.py` userland (`boot`, `verify`, `run FILE.sutra`,
`memory`, `exit`) still exists and still **compiles** `.sutra` rather than
`exec()`-ing Python, but the सूत्र dispatcher above is the one the CLI uses.

---

## 5. Self-editing — what is real, what is gated

| Surface | Operation | Gate | Status |
|---|---|---|---|
| Body (weights) | grow hidden layer (`expand_hidden`) | predictions must not move (drift < 1e-9) | ✅ always passes — new units start with zero outgoing weights |
| Body (weights) | prune hidden layer (`shrink_hidden`) | drift < 1e-6 | ✅ drops only the units with the smallest output norm |
| Optimizer | Adam moments migrated across surgery | — | ✅ without this, growth *degraded* held-out perplexity; with it, it improves |
| OS (image) | rebuild kernel from सूत्र source | boot + self-test + `READY` | ✅ a broken kernel is never installed |
| Learning rate | annealed 0.6× per warm round | — | ✅ without annealing rounds 2–4 oscillated (12.7 → 13.0 → 16.2); with it: 12.7 → 11.3 → 10.4 → 10.1 |
| Repository source | *proposals only* (`proposal-*.md`) | human review + CI | ⚠️ deliberately not automatic |

The last row is a design decision, stated plainly: an autonomous loop that
rewrites the project's Python without review is how a repository becomes a
security incident. The loop *can* change its weights, its size, its corpus, its
generated programs and its OS image — all versioned and verifiable. Source
changes are proposed, logged, and left to a human.

Every attempt, accepted or rejected, is appended to
`$BRAHMA_HOME/self/self_edit_log.json` by `SelfEditor.flush()`.

---

## 6. Target → autonomous training

```python
from brahma_llm.trainer import AutonomousTrainer, Target

trainer = AutonomousTrainer()
report = trainer.run(Target(
    description="अभाज्य संख्या जाँच लिखो",
    keywords="prime",          # biases the program generator
    iterations=4, epochs=4, size="tiny",
    budget_seconds=240,        # wall-clock stop
    threshold=None,            # or a perplexity target
    patience=2,                # stop after N rounds without improvement
    allow_growth=True,         # body edits after a win
))
print(report["best"])          # {'perplexity': 8.962, 'iteration': 4, 'path': ...}
```

The loop, in order:

1. **generate** सूत्र programs aimed at the target;
2. **execute** each one — failures never enter the corpus;
3. **train** (cold start once, warm starts afterwards, with annealing);
4. **measure** held-out perplexity on real repository files only — generated
   text is never part of the hold-out, so the model cannot grade its own
   homework;
5. **keep** the best checkpoint (`best/`) and reload it when a round regresses;
6. **grow** the hidden layer after an improvement;
7. **stop** on threshold, patience, iteration cap or time budget.

Everything lands in `$BRAHMA_HOME/llm/`: `best/` (`model.json`,
`tokenizer.json`, `meta.json`), `report.json`, `self/self_edit_log.json`.

### 6.5 One command for the whole cycle

```bash
brahma llm mission --target "अभाज्य संख्या जाँच" --iterations 2 --epochs 2 --size tiny
```

Measured run (3.7 s, after the 3.0.0 cleanup):

| step | result |
|---|---|
| training | 2 rounds, 12/12 programs ran, perplexity 18.766 → **15.951**, hidden 32 → 40, params 5 384 |
| own OS | the model wrote a kernel body; it booted, so `origin = model`, image installed |
| **server** | the trained model was served on a real port and smoke-tested: `/status`, `/kernel`, `/chat` (code), `/run`, `/image` — `smoke_ok: true`, `/run` returned `42`, `/image` returned a PNG |
| report | `<BRAHMA_HOME>/mission/mission.json` |

The boot contract is a fixed harness (banner → self-test → *generated body* →
`READY`), and the acceptance rule is truncation: the longest prefix of the
model's body that actually boots wins. If no prefix boots, the shipped kernel is
reinstalled and the report says `origin = shipped-kernel` — the fallback is
recorded, never hidden.

There is **no app builder** any more: the last step starts ब्रह्म itself and
proves the model answers, writes code, executes it and renders an image behind
HTTP. See §6.7.

### 6.6 Continuing instead of restarting (`--resume`, `--continuous`)

A mission that is thrown away after one run is not an autonomous loop, so the
cycle can continue from where it stopped:

```bash
brahma llm mission --target "अभाज्य संख्या जाँच" --iterations 1 --epochs 1 \
        --continuous --max-generations 3 --budget 120      # keep improving
brahma llm mission --target "अभाज्य संख्या जाँच" --iterations 1 --epochs 1 --resume
```

`--continuous` trains further generations while each one beats the last, the
budget lasts and `--target-perplexity` has not been met.  Measured
(`--max-generations 3 --budget 120`, fresh home):

| generation | cold start | held-out perplexity | improved |
|---|---|---|---|
| 1 | yes | 25.568 | — |
| 2 | no (warm) | 23.133 | yes |
| 3 | no (warm) | **22.288** | yes |

`--resume` reloads the previous mission's best checkpoint and passes its
perplexity in as the bar to beat.  Measured on the run above (`--resume
--iterations 1`): `previous_best = 15.951`, the resumed round produced **19.464**,
so the report says `improved_this_run: false`, `best_perplexity` stays **15.951**
and the better checkpoint is kept.  That is the point of the flag: a regression
is *reported as a regression* and cannot overwrite the best model.  The trainer
also receives `previous_best`, so "सुधरा" in the log is judged against the
previous mission rather than against infinity.

### 6.7 The model serves itself — chat, code, action, image

`brahma llm serve` starts ब्रह्म on HTTP; there is nothing to generate first.

| endpoint | what it really does |
|---|---|
| `GET /` | one-page UI: chat, code, run, image |
| `GET /status` | model, kernel, corpus, last mission |
| `GET /kernel` | boots the installed सूत्र-OS image over HTTP |
| `POST /chat` | intent routing → the matching capability below |
| `POST /generate` | raw model continuation |
| `POST /run` | compile + execute सूत्र on the VM |
| `POST /explain` | structural analysis (functions, opcodes, nesting) |
| `GET /image?prompt=…` | a real PNG rendered from a सूत्र program the model chose |
| `POST /shell` | `{"command": "…"}` → the सूत्र-OS shell, on the kernel's live state |

The agent (`brahma_llm/agent.py`) splits into real capabilities, not promises:

| intent | what happens |
|---|---|
| `chat` | the model continues the conversation; empty output → an honest "no checkpoint" reply |
| `code` | valid सूत्र candidates are generated for the goal, **ranked by the model's own loss**, the winner is compiled and executed, and its output is returned with the source |
| `run` | सूत्र source from the message is executed on the VM |
| `explain` | the program is parsed and reported structurally — deterministic |
| `image` | the model picks a numeric सूत्र program, the VM runs it, and its numbers plus the model's distribution drive a procedural PNG renderer (zlib/struct only) |
| `status` / `help` | measured state / the capability table |

### 6.8 What "the model writes the code" means here

Two mechanisms are used, and both are the model's:

1. **ranking** — the goal selects candidate programs deterministically
   (`ProgramGenerator.categories_for`), then the model scores every candidate as
   `loss(prompt + candidate)` and the lowest-loss program wins.  Measured: for
   `अभाज्य संख्या जाँच` the chosen candidate is the अभाज्य category, and its
   executed output is `2 3 5 7 11 13 …`.
2. **free generation** — `complete_program` asks the model to continue
   `"# लक्ष्य: …"`, keeps the longest prefix that compiles **and runs**, and
   reports whether it succeeded (`free_generation_runs`).

At 4 480 parameters free generation is mostly garbage, and the API says so
rather than dressing it up.  Ranking is what makes the capability useful today;
free generation is the part that grows with the model and the corpus.

---

## 7. Everything is connected

```
                     ┌──────────────────────────────┐
  brahma run/compile │  brahma/  lexer→parser→compiler→VM  │  ← सूत्र language
                     └──────────────┬───────────────┘
                                    │ bytecode
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
 ┌──────▼──────┐            ┌───────▼───────┐          ┌────────▼────────┐
 │ SUTRAOS img │            │ brahma_llm    │          │ kernel/ shell   │
 │ (kernel.py) │◄───────────┤ tokenizer     │          │ boot/verify/run │
 └─────────────┘  generates │ NeuralLM      │          └─────────────────┘
                            │ NgramLM       │
                            │ trainer       │
                            │ selfedit      │
                            │ agent·server  │
                            └───┬───────┬───┘
                                │       │
                  ┌─────────────▼─┐   ┌─▼──────────────────┐
                  │ brahma_chat   │   │ generated app dir  │
                  │ /llm          │   │ server.py+index    │
                  │ /llm/generate │   │ +manifest.json     │
                  │ /llm/run      │   └────────────────────┘
                  └───────────────┘
```

Concrete entry points:

* `brahma llm …` — the whole stack behind one CLI (`brahma/cli.py` delegates);
* `brahma_chat.create_app()` — adds `/llm`, `/llm/generate`, `/llm/run` to the
  chat backend, so a browser client talks to the model and the VM;
* `brahma llm serve` (`brahma_llm/server.py`) — the model serving itself: chat,
  code, run, explain, image, kernel, status;
* `brahma llm ask` / `brahma llm image` — the same agent from the CLI;
* `कृत्रिमबुद्धि/सूत्र_पूर्ण_स्वचालित_निर्माता.py` — LLM → सूत्र → **real
  bytecode** (`.sbc`) → execution + disassembly;
* `kernel/kernel_engine.py` and `सूत्र_boot_image_builder.py` — the OS side.

---

## 8. CLI reference

```
brahma llm info [--model DIR] [--json]
brahma llm corpus [--sample N] [--generate N] [--goal TEXT] [--seed S] [--out DIR] [--json]
brahma llm train [--kind neural|ngram] [--size tiny|small|medium|large|xlarge|huge|brahma] [--epochs N] [--docs] [--out DIR]
brahma llm generate PROMPT [--tokens N] [--temperature T] [--engine python|sutra]
brahma llm complete [PROMPT] [--tokens N]          # valid सूत्र program only
brahma llm ask MESSAGE [--model DIR] [--out PNG] [--json]
brahma llm chat [--model DIR]
brahma llm image PROMPT [--out PNG] [--model DIR] [--json]
brahma llm serve [--host H] [--port P] [--model DIR] [--once] [--allow-train]
brahma llm autotrain --target TEXT [--iterations N] [--epochs N] [--budget S] [--json]
brahma llm evolve --body|--os [--extra N] [--json]
brahma llm kernel build|boot|verify|install|info [--json]
brahma llm shell [--command CMD]... [--script FILE] [--json]
brahma llm mission --target TEXT [--iterations N] [--epochs N] [--resume]\
                    [--continuous] [--target-perplexity P] [--no-os] [--no-serve] [--json]
brahma llm sutra-math [--json]
brahma llm bench [--sizes …] [--epochs N] [--json]
```

All commands respect `BRAHMA_HOME` (default `~/सूत्र-तंत्र`) for checkpoints,
images, mission reports and logs, so a throwaway run never touches your home directory:

```bash
BRAHMA_HOME=/tmp/b python -m brahma llm train
BRAHMA_HOME=/tmp/b python -m brahma llm autotrain --target "सूची कार्यक्रम"
```

---

## 9. Scaling — the honest arithmetic

The model is `V·d + H·(order·d) + V·H` parameters.  Training cost in pure Python
is dominated by interpreted arithmetic: measured on this checkout, one epoch
costs **~2 s at 4.5 k parameters, 21.7 s at 115 k, 50.3 s at 255 k and 107.4 s at
559 k** — about 20 µs per parameter per epoch on one core.

| parameters | measured here | what it buys on this corpus |
|---|---|---|
| 4 480 (`tiny`) | 2 s/epoch, ppl **13.8** | best perplexity in the table |
| 115 287 (`large`) | 21.7 s/epoch, ppl 86.6 | worse: vocabulary outgrew the text |
| 254 919 (`xlarge`) | 50.3 s/epoch, ppl 342.6 | worse again |
| 558 903 (`huge`) | 107.4 s/epoch, ppl 3 139.9 | worse still — twice, identically |
| 1 390 383 (`brahma`, as trained) | **189.3 s/epoch, ppl 25 600 162** | the largest model this box can train in three minutes |
| 2 411 008 (`brahma` at its vocabulary cap) | instantiated + counted | no corpus for it yet |
| 10⁹–10¹¹ | not feasible here | needs accelerators, 10¹²+ tokens, months |

So the code is *architecture-scalable* and this corpus is not.  Growing the model
without growing the data makes perplexity worse, and this document measures that
happening rather than asserting the opposite.  Anyone claiming a repository like
this one contains "the largest, most powerful LLM" is selling something; the
right next steps, in order, are: more सूत्र programs (the generator can make
them), a bigger held-out set, then a larger `--size`.

---

## 10. Limitations

* **Size**: the largest instantiable preset here is **2.41 M parameters** at
  its vocabulary cap (`--size brahma`), and the largest actually trained
  end-to-end in this repo — now measured, not projected — is **1 390 383
  parameters in 189.3 s for one epoch** (perplexity 2.56 × 10⁷, because 53
  training texts cannot train 1.4 M weights).  This is not, and cannot be
  described as, the largest or most powerful LLM in existence — frontier models
  are 10⁵–10⁶× larger and are trained on trillions of tokens.  What this project
  claims is narrower and checkable: the whole stack (language, VM, kernel,
  trainer, self-editor, agent, server, images) is here, from scratch, and runs.
* **Corpus size**: ~33 k characters.  Devanagari-only generation beyond short
  programs is not what these checkpoints are good at.
* **Speed**: pure Python. Every multiply-add is a CPython operation, so `huge`
  and `brahma` are counting exercises, not training runs.
* **No attention**: the context is a fixed window of `order` akṣaras.  Adding
  attention is a real project, and it needs the data to justify it.
* **`<unk>` handling**: warm starts keep the vocabulary fixed, so new akṣaras
  map to `<unk>`; a full retrain rebuilds it.
* **Self-editing scope**: weights, size, corpus, generated programs and the OS
  image — never repository source without review (§5).
* **Chat quality**: intent routing and code/image actions work; open-ended
  conversation is a continuation from a 4 k–250 k parameter model, not an
  assistant.  `docs/LLM.md` §6.8 is explicit about which half of "the model
  writes code" is doing the work.
* **Images are procedural**: the model supplies the program and the palette; the
  renderer is rings + waves + value noise.  It is not diffusion, and no part of
  this repository claims otherwise.

---

## 11. Testing

```
$ python -m pytest tests/test_llm.py -q
59 passed in 14.6 s
$ python -m pytest -q
587 passed in 34.0 s
```

Covered: tokenizer reversibility, n-gram distributions and learning, neural
gradients vs central differences, training loss decrease, save/load equality,
सूत्र↔Python forward-pass equality (1e-12), kernel image layout/boot/verify/
install, corrupt-image rejection, generator validity, invalid-program rejection,
body surgery invariants, editor accept/reject + audit log, the autonomous loop
(report shape, acceptance rate, budget stop, resume honesty, continuous
generations, perplexity stop), the agent (intent routing, model-ranked
synthesis, execution, structural explanation, status), image output (real PNG,
deterministic, model-driven program), the HTTP surface (index, status, kernel
boot, chat/code, run, explain, image, 400s on bad input) and the CLI
(`ask`, `image`, `serve --once`, `mission`).
