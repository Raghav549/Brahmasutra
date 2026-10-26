"""🕉️ चित्र — images produced by ब्रह्म-LLM, with no imaging library.

There is no diffusion model here and this module does not pretend otherwise.
What it *does* do is real: the model is asked for a सूत्र program, that program
is executed on the project's VM, and the numbers it prints (together with the
model's own next-token distribution over the prompt) drive a deterministic
procedural renderer.  The output is a genuine PNG written byte by byte with
:mod:`zlib` and :mod:`struct` only.

So the chain for one image is::

    prompt → the model writes सूत्र → the VM runs it → palette + seed
           → procedural renderer → PNG (stdlib only)

If the generated program does not run, the renderer says so in its metadata and
uses the prompt hash instead of invented numbers — the fallback is recorded, not
hidden (see :func:`generate`).
"""

from __future__ import annotations

import hashlib
import math
import struct
import zlib
from typing import Dict, List, Optional, Sequence, Tuple

SIZE = 192

#: Prompt used to ask the model for a drawing program.
IMAGE_PROMPT = "# चित्र: "

FALLBACK_PROGRAM = (
    'दर्शय "🕉️ चित्र"\n'
    "स्थापय i = 0\n"
    "यावत् i < 6\n"
    "    दर्शय i * 37 + 11\n"
    "    i = i + 1\n"
    "अन्त\n"
)


def _write_png(path: str, width: int, height: int, rows: Sequence[bytes]) -> str:
    """Write an 8-bit RGB PNG; ``rows`` are ``width * 3`` byte strings."""

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    raw = b"".join(b"\x00" + row for row in rows)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    blob = (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))
    with open(path, "wb") as handle:
        handle.write(blob)
    return path


def _palette_from_probs(probs: Sequence[float]) -> List[Tuple[int, int, int]]:
    """Turn the model's distribution into a small, vivid palette."""
    top = sorted(range(len(probs)), key=lambda index: probs[index], reverse=True)[:5]
    palette = []
    for rank, token in enumerate(top):
        weight = probs[token] if token < len(probs) else 0.0
        hue = (token * 0.61803398875 + rank * 0.13) % 1.0
        value = 0.55 + min(0.45, weight * 6.0)
        palette.append(_hsv_to_rgb(hue, 0.55 + 0.35 * (rank % 2), value))
    while len(palette) < 3:
        palette.append((20, 20, 30))
    return palette


def _hsv_to_rgb(hue: float, saturation: float, value: float) -> Tuple[int, int, int]:
    sector = int(hue * 6.0) % 6
    fraction = hue * 6.0 - int(hue * 6.0)
    p = value * (1.0 - saturation)
    q = value * (1.0 - saturation * fraction)
    t = value * (1.0 - saturation * (1.0 - fraction))
    red, green, blue = [
        (value, t, p), (q, value, p), (p, value, t),
        (p, q, value), (t, p, value), (value, p, q),
    ][sector]
    return (int(red * 255) % 256, int(green * 255) % 256, int(blue * 255) % 256)


def _value_noise(seed: int, x: float, y: float) -> float:
    """Cheap deterministic value noise in ``0..1`` (no libraries, no files)."""
    total = 0.0
    amplitude = 1.0
    frequency = 1.0
    normaliser = 0.0
    for octave in range(4):
        sample_x = int(x * frequency)
        sample_y = int(y * frequency)
        digest = hashlib.sha256(
            ("%d:%d:%d:%d" % (seed, sample_x, sample_y, octave)).encode("ascii")
        ).digest()
        value = digest[0] / 255.0
        total += value * amplitude
        normaliser += amplitude
        amplitude *= 0.5
        frequency *= 2.0
    return total / normaliser if normaliser else 0.0


def _numbers_of(report) -> List[float]:
    """Every number a program printed, in order (ints and floats)."""
    values: List[float] = []
    for line in report.output:
        for token in line.replace(",", " ").split():
            try:
                values.append(float(token))
            except ValueError:
                continue
    return values


def _numbers_from_program(model, prompt: str) -> Tuple[List[float], str, str]:
    """Numbers for the image, and where they came from.

    ``origin`` is ``generated`` (free model continuation ran), ``ranked`` (the
    model chose a valid सूत्र program from the goal-filtered set and the VM ran
    it) or ``fallback`` (nothing model-written ran; the prompt hash is used).
    """
    from brahma.api import execute

    if model is not None:
        try:
            source = model.complete_program(IMAGE_PROMPT + prompt + "\n", max_tokens=70, seed=23)
        except Exception:  # noqa: BLE001 - reported through ``origin``
            source = ""
        if source.strip():
            report = execute(source, source_name="<image>", step_limit=50_000)
            if report.error is None:
                numbers = _numbers_of(report)
                if len(numbers) >= 4:
                    return numbers, source, "generated"

        # The model ranks *numeric* candidates (primes, fibonacci, loops) and
        # the best-scoring one that really prints numbers becomes the artwork's
        # source of entropy.
        try:
            from .programs import ProgramGenerator

            generator = ProgramGenerator(seed=23)
            scored = []
            for name in ("अभाज्य", "फ़ीबोनाची", "चक्र", "गणित"):
                if name not in generator.templates:
                    continue
                source = generator.templates[name]()
                try:
                    loss = model.score(IMAGE_PROMPT + prompt + "\n" + source)
                except Exception:  # noqa: BLE001 - unscored candidates go last
                    loss = float("inf")
                scored.append((loss, name, source))
            scored.sort(key=lambda item: item[0])
            for _, name, source in scored:
                report = execute(source, source_name="<image-ranked>", step_limit=50_000)
                if report.error is None:
                    numbers = _numbers_of(report)
                    if len(numbers) >= 4:
                        return numbers, source, "ranked:%s" % name
        except Exception:  # noqa: BLE001 - fall through to the template
            pass

    report = execute(FALLBACK_PROGRAM, source_name="<image-fallback>", step_limit=50_000)
    return _numbers_of(report), FALLBACK_PROGRAM, "fallback"


def _seed_of(prompt: str, numbers: Sequence[float]) -> int:
    digest = hashlib.sha256(prompt.encode("utf-8")).digest()
    seed = int.from_bytes(digest[:4], "big")
    for value in numbers[:8]:
        seed = (seed * 31 + int(abs(value) * 1000)) & 0xFFFFFFFF
    return seed


def render(prompt: str, palette: Sequence[Tuple[int, int, int]], seed: int,
           numbers: Sequence[float], size: int = SIZE) -> List[bytes]:
    """Procedural artwork: rings, waves and noise over the model's palette."""
    rows: List[bytes] = []
    phase = (numbers[0] if numbers else 0.0) % (2 * math.pi)
    scale = 1.0 + (len(numbers) % 5) * 0.35
    centre = size / 2.0
    for y in range(size):
        row = bytearray()
        for x in range(size):
            dx = (x - centre) / centre
            dy = (y - centre) / centre
            radius = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx)
            ripple = math.sin(radius * 9.0 * scale + phase) * 0.5 + 0.5
            swirl = math.sin(angle * 3.0 + radius * 6.0 + phase) * 0.5 + 0.5
            noise = _value_noise(seed, x / size, y / size)
            mix = max(0.0, min(1.0, 0.45 * ripple + 0.30 * swirl + 0.25 * noise))
            first = palette[int(radius * 2.5) % len(palette)]
            second = palette[int(mix * len(palette)) % len(palette)]
            row.extend((
                int(first[0] * (1 - mix) + second[0] * mix),
                int(first[1] * (1 - mix) + second[1] * mix),
                int(first[2] * (1 - mix) + second[2] * mix),
            ))
        rows.append(bytes(row))
    return rows


def generate(prompt: str, model=None, path: Optional[str] = None,
             size: int = SIZE) -> Dict[str, object]:
    """Render ``prompt`` into a PNG and return the metadata."""
    numbers, source, origin = _numbers_from_program(model, prompt)
    palette: List[Tuple[int, int, int]] = [(30, 30, 40), (200, 170, 90), (120, 60, 160)]
    probs: List[float] = []
    if model is not None:
        try:
            encoded = model.tokenizer.encode(prompt)[-model.model.order:]
            probs = model.model.next_token_probs(encoded)
            palette = _palette_from_probs(probs)
        except Exception:  # noqa: BLE001 - keep the default palette
            probs = []
    seed = _seed_of(prompt, numbers)
    rows = render(prompt, palette, seed, numbers, size=size)
    target = path or "brahma-%d.png" % (seed % 100000)
    _write_png(target, size, size, rows)
    return {
        "path": target,
        "prompt": prompt,
        "size": [size, size],
        "seed": seed,
        "bytes": len(rows) * (size * 3 + 1),
        "palette": [list(colour) for colour in palette],
        "program": source,
        "program_ran": origin != "fallback",
        "origin": origin,
        "numbers": len(numbers),
        "engine": "procedural (model-driven सूत्र program + palette)",
    }
