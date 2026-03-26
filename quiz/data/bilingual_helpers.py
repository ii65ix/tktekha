"""Helpers to build bilingual MCQs with matching EN/AR option pairs."""

from __future__ import annotations

import random
from typing import Iterable


def shuffle_preserve_pairs(
    q_en: str,
    q_ar: str,
    options: list[tuple[str, str]],
    correct_index_1based: int,
    rng: random.Random,
) -> dict:
    """Shuffle four (en, ar) option pairs; return dict for Question model fields."""
    if len(options) != 4:
        raise ValueError("Need exactly 4 options")
    correct_pair = options[correct_index_1based - 1]
    pairs = list(options)
    rng.shuffle(pairs)
    correct_new = pairs.index(correct_pair) + 1
    d = {
        "text": q_en,
        "text_ar": q_ar,
        "correct_answer": correct_new,
    }
    for i, (en, ar) in enumerate(pairs, start=1):
        d[f"option{i}"] = en
        d[f"option{i}_ar"] = ar
    return d


def pick_three_wrong(
    pool: list[tuple[str, str]],
    exclude: tuple[str, str],
    rng: random.Random,
) -> list[tuple[str, str]]:
    wrong = [p for p in pool if p != exclude]
    rng.shuffle(wrong)
    return wrong[:3]
