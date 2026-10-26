"""🕉️ ब्रह्म टोकनाइज़र — a tokenizer built for the सूत्र language.

Most tokenizers are trained on English and shred Devanagari into individual
code points, which throws away the *akṣara* (अक्षर) — the unit a Sanskrit
reader actually perceives.  This tokenizer keeps aksharas together:

* a consonant cluster ``क् + ष`` is one token, with its matra/anusvāra attached
  (``क्षि``, ``कं``);
* ASCII words, numbers and punctuation become their own tokens;
* every token keeps its source text, so :meth:`SutraTokenizer.decode` is exact
  for in-vocabulary text and lossless apart from ``<unk>``.

The class is dependency-free and deterministic; :meth:`fit` counts n-grams for
:class:`brahma_llm.model.NgramLM` at the same time so both models share one
vocabulary.

    >>> t = SutraTokenizer().fit(["दर्शय \\"नमस्ते\\""])
    >>> t.decode(t.encode("दर्शय नमस्ते")) == "दर्शय नमस्ते"
    True
"""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from typing import Dict, Iterable, List, Optional, Sequence

PAD, UNK, BOS, EOS = "<pad>", "<unk>", "<bos>", "<eos>"
SPECIALS = (PAD, UNK, BOS, EOS)

#: Devanagari consonants (including the nukta forms क़ … य़).
CONSONANTS = set(
    "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
    "क़ख़ग़ज़ड़ढ़फ़य़ळऱऩ"
)
#: Independent vowels — they never join the previous cluster.
VOWELS = set("अआइईउऊऋॠऌॡएऐओऔऍऑऎऒ")
VIRAMA = "\u094d"
#: Marks that stay glued to the preceding cluster (matras, anusvāra, nukta …).
GLUE_CATEGORIES = ("Mn", "Mc", "Me")
DEVANAGARI_DIGITS = set("०१२३४५६७८९")


def _is_devanagari_letter(ch: str) -> bool:
    return "\u0900" <= ch <= "\u097f"


def _is_glue(ch: str) -> bool:
    return unicodedata.category(ch) in GLUE_CATEGORIES or ch == VIRAMA or _is_devanagari_letter(ch)


def aksharas(text: str) -> List[str]:
    """Split ``text`` into akshara-ish tokens without a vocabulary.

    The split is reversible: ``"".join(aksharas(s)) == s`` for every string.
    """
    out: List[str] = []
    index = 0
    length = len(text)
    while index < length:
        ch = text[index]
        if ch in CONSONANTS or ch == "ॐ":
            start = index
            index += 1
            while index < length:
                nxt = text[index]
                if nxt == VIRAMA and index + 1 < length and text[index + 1] in CONSONANTS:
                    index += 2  # consonant + virama + consonant join the cluster
                    continue
                if unicodedata.category(nxt) in GLUE_CATEGORIES or nxt == VIRAMA:
                    index += 1
                    continue
                break
            out.append(text[start:index])
        elif ch in VOWELS:
            start = index
            index += 1
            while index < length and unicodedata.category(text[index]) in GLUE_CATEGORIES:
                index += 1
            out.append(text[start:index])
        elif ch in DEVANAGARI_DIGITS:
            start = index
            while index < length and text[index] in DEVANAGARI_DIGITS:
                index += 1
            out.append(text[start:index])
        elif ch.isascii() and (ch.isalnum() or ch == "_"):
            start = index
            while index < length and text[index].isascii() and (text[index].isalnum() or text[index] == "_"):
                index += 1
            out.append(text[start:index])
        elif ch == " ":
            start = index
            while index < length and text[index] == " ":
                index += 1
            out.append(text[start:index])
        else:
            out.append(ch)
            index += 1
    return out


class SutraTokenizer:
    """Akshara-level tokenizer with a frequency-pruned vocabulary."""

    def __init__(self, tokens: Optional[Sequence[str]] = None, min_count: int = 1, max_vocab: int = 4096):
        self.min_count = min_count
        self.max_vocab = max_vocab
        self.tokens: List[str] = list(tokens or SPECIALS)
        self._index: Dict[str, int] = {token: i for i, token in enumerate(self.tokens)}
        self.counts: Counter = Counter()

    # -- vocabulary ------------------------------------------------------
    def fit(self, texts: Iterable[str], min_count: Optional[int] = None, max_vocab: Optional[int] = None) -> "SutraTokenizer":
        """Build the vocabulary from ``texts`` (largest requested first)."""
        min_count = self.min_count if min_count is None else min_count
        max_vocab = self.max_vocab if max_vocab is None else max_vocab
        counts: Counter = Counter()
        for text in texts:
            counts.update(aksharas(text))
        kept = [token for token, count in counts.most_common() if count >= min_count]
        kept = kept[: max(1, max_vocab - len(SPECIALS))]
        self.counts = counts
        self.tokens = list(SPECIALS) + sorted(kept)
        self._index = {token: i for i, token in enumerate(self.tokens)}
        return self

    # -- ids -------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.tokens)

    @property
    def vocab_size(self) -> int:
        return len(self.tokens)

    @property
    def pad_id(self) -> int:
        return self._index[PAD]

    @property
    def unk_id(self) -> int:
        return self._index[UNK]

    @property
    def bos_id(self) -> int:
        return self._index[BOS]

    @property
    def eos_id(self) -> int:
        return self._index[EOS]

    def token_id(self, token: str) -> int:
        return self._index.get(token, self.unk_id)

    def encode(self, text: str, add_special: bool = False) -> List[int]:
        """Text → ids (``<bos>``/``<eos>`` added when ``add_special``)."""
        ids = [self.token_id(token) for token in aksharas(text)]
        if add_special:
            return [self.bos_id] + ids + [self.eos_id]
        return ids

    def decode(self, ids: Iterable[int], skip_special: bool = True) -> str:
        """Ids → text."""
        special_ids = {self._index[name] for name in SPECIALS}
        parts: List[str] = []
        for index in ids:
            if index < 0 or index >= len(self.tokens):
                continue
            token = self.tokens[index]
            if skip_special and index in special_ids:
                continue
            if token == UNK:
                parts.append("�")
            else:
                parts.append(token)
        return "".join(parts)

    # -- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "tokens": self.tokens,
            "min_count": self.min_count,
            "max_vocab": self.max_vocab,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SutraTokenizer":
        return cls(tokens=data["tokens"], min_count=data.get("min_count", 1),
                   max_vocab=data.get("max_vocab", 4096))

    def save(self, path: str) -> str:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=1)
        return path

    @classmethod
    def load(cls, path: str) -> "SutraTokenizer":
        with open(path, "r", encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))
