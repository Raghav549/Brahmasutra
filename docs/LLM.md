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

| preset | d_model | hidden | order | vocab cap | params (measured) |
|---|---|---|---|---|---|
| `tiny` | 8 | 32 | 2 | 96 | 4 480 |
| `small` | 16 | 64 | 3 | 160 | 16 096 |
| `medium` | 24 | 128 | 4 | 256 | 51 584 |
| `large` | 32 | 192 | 5 | 384 | (scales as `V·H + H·(order·d)` ) |

`brahma llm info` always prints the **counted** parameter total of the loaded
checkpoint rather than a marketing number.

---

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

`brahma_llm/kernel.py` compiles a सूत्र program (`KERNEL_SOURCE`) to the project's
bytecode and wraps it in the documented image format:

```
"SUTRAOS" | version (>I) | payload length (>I) | bytecode
```

The boot contract is enforced by `verify()`: banner → self-test line
`स्व-परीक्षण: ठीक / ठीक` → `READY`. `install()` refuses to write an image that
fails it.

```
$ brahma llm kernel verify
🕉️ सूत्र-OS कर्नेल प्रारम्भ
स्व-परीक्षण: ठीक / ठीक
स्मृति इकाइयाँ: 7
READY
  चरण: 143, छवि: 10059 बाइट, स्थिति: ठीक
```

The shell in `kernel/kernel_engine.py` is a real userland for it — `boot`,
`verify`, `run FILE.sutra`, `memory`, `exit`. `.sutra` files are **compiled**;
the old implementation `exec()`-ed arbitrary files as Python, which is gone.

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

Measured run (2.9 s):

| step | result |
|---|---|
| training | 2 rounds, 12/12 programs ran, perplexity 15.313 → **14.006**, hidden 32 → 40 |
| own OS | the model wrote a kernel body; it booted, so `origin = model`, image installed |
| app | logic **generated** by the model, ran, `/status` + `/run` smoke tests passed |
| report | `<BRAHMA_HOME>/mission/mission.json` |

The boot contract is a fixed harness (banner → self-test → *generated body* →
`READY`), and the acceptance rule is truncation: the longest prefix of the
model's body that actually boots wins. If no prefix boots, the shipped kernel is
reinstalled and the report says `origin = shipped-kernel` — the fallback is
recorded, never hidden.

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
                            │ app_builder   │
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
* `brahma llm build-app` / `कृत्रिमबुद्धि/सूत्र_अनुप्रयोग_निर्माता.py` — the app
  builder is now LLM-driven and smoke-tested;
* `कृत्रिमबुद्धि/सूत्र_पूर्ण_स्वचालित_निर्माता.py` — LLM → सूत्र → **real
  bytecode** (`.sbc`) → execution + disassembly;
* `kernel/kernel_engine.py` and `सूत्र_boot_image_builder.py` — the OS side.

---

## 8. CLI reference

```
brahma llm info [--model DIR] [--json]
brahma llm corpus [--sample N] [--json]
brahma llm train [--kind neural|ngram] [--size tiny|small|medium|large] [--epochs N] [--docs] [--out DIR]
brahma llm generate PROMPT [--tokens N] [--temperature T] [--engine python|sutra]
brahma llm complete [PROMPT] [--tokens N]          # valid सूत्र program only
brahma llm chat [--once]
brahma llm autotrain --target TEXT [--iterations N] [--epochs N] [--budget S] [--json]
brahma llm evolve --body|--os [--extra N] [--json]
brahma llm kernel build|boot|verify|install|info [--json]
brahma llm build-app --target TEXT [--out DIR] [--port P] [--json]
brahma llm mission --target TEXT [--iterations N] [--epochs N] [--no-os] [--no-app] [--json]
brahma llm sutra-math [--json]
brahma llm bench [--sizes …] [--epochs N] [--json]
```

All commands respect `BRAHMA_HOME` (default `~/सूत्र-तंत्र`) for checkpoints,
apps, images and logs, so a throwaway run never touches your home directory:

```bash
BRAHMA_HOME=/tmp/b python -m brahma llm train
BRAHMA_HOME=/tmp/b python -m brahma llm autotrain --target "सूची कार्यक्रम"
```

---

## 9. Scaling — the honest arithmetic

The model is `V·d + H·(order·d) + V·H` parameters. Training cost in pure Python
is roughly **10–30 µs per parameter per epoch** on one core (measured: 16 k
parameters × 4 epochs ≈ 11 s). That gives:

| parameters | realistic pure-Python training time | what it would buy on this corpus |
|---|---|---|
| 5 k (tiny) | seconds | memorises patterns, generates short valid programs |
| 50 k (medium) | ~35 s for 4 epochs | better local syntax, more overfitting |
| 1 M | hours per epoch | pointless without more data |
| 10⁹–10¹¹ | not feasible here | needs accelerators, 10¹²+ tokens, and months |

So the code is *architecture-scalable* and the corpus is not. Growing the model
without growing the data makes perplexity worse — §3.1 shows that happening.
Anyone claiming otherwise is selling something; this document measures it
instead. The right next steps, in order, are: more सूत्र programs (the generator
can make them), a bigger held-out set, then a larger `--size`.

---

## 10. Limitations

* **Corpus size**: ~33 k characters. Devanagari-only text generation beyond
  short programs is not what this checkpoint is good at.
* **Speed**: pure Python. A pure-Python softmax over a 96-token vocabulary is
  fine; over 50 k tokens it is not. `NgramLM` exists for fast baselines.
* **No attention**: the context is a fixed window of `order` akṣaras. Adding
  attention is a real project (and needs the data to justify it).
* **`<unk>` handling**: warm starts keep the vocabulary fixed, so new akṣaras
  map to `<unk>`; a full retrain rebuilds it.
* **Self-editing scope**: weights, size, corpus, generated programs and the OS
  image — never repository source without review (§5).
* **Not a chatbot**: `brahma llm chat` generates continuations; it does not do
  instruction following, RLHF, or tool use beyond the VM.

---

## 11. Testing

```
$ python -m pytest tests/test_llm.py -q
44 passed in 6.3 s
```

Covered: tokenizer reversibility, n-gram distributions and learning, neural
gradients vs central differences, training loss decrease, save/load equality,
सूत्र↔Python forward-pass equality (1e-12), kernel image layout/boot/verify/
install, corrupt-image rejection, generator validity, invalid-program rejection,
body surgery invariants, editor accept/reject + audit log, the autonomous loop
(report shape, acceptance rate, budget stop), app-builder smoke tests and the
CLI wiring (`brahma llm …`) and the one-command mission (whole cycle, honest
`model`/`shipped-kernel` fallback).
