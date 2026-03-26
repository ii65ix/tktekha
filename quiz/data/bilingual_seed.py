"""Bilingual question bank: 7×50 = 350 (EN + AR), with category metadata."""

from __future__ import annotations

import random
from typing import Iterator

from quiz.data.bilingual_beauty import generate_beauty
from quiz.data.bilingual_cars import generate_cars
from quiz.data.bilingual_general import generate_general
from quiz.data.bilingual_geo import generate_geography
from quiz.data.bilingual_movies import generate_movies
from quiz.data.bilingual_science import generate_science
from quiz.data.bilingual_sports import generate_sports

# (display name EN, slug, name AR) — order is stable for seeding
BILINGUAL_CATEGORIES: list[tuple[str, str, str]] = [
    ("Cars", "cars", "السيارات"),
    ("Sports", "sports", "الرياضة"),
    ("General Knowledge", "general-knowledge", "المعرفة العامة"),
    ("Geography", "geography", "الجغرافيا"),
    ("Beauty & Lifestyle", "beauty-lifestyle", "الجمال ونمط الحياة"),
    ("Science", "science", "العلوم"),
    ("Movies", "movies", "الأفلام"),
]

_SLUG_TO_GENERATOR = {
    "cars": generate_cars,
    "sports": generate_sports,
    "general-knowledge": generate_general,
    "geography": generate_geography,
    "beauty-lifestyle": generate_beauty,
    "science": generate_science,
    "movies": generate_movies,
}


def iter_bilingual_seed(
    rng: random.Random | None = None,
) -> Iterator[tuple[str, dict]]:
    """Yield (category_slug, question_dict) for all 350 questions."""
    _ = rng  # generators use their own fixed RNGs for reproducibility
    for _name_en, slug, _name_ar in BILINGUAL_CATEGORIES:
        gen = _SLUG_TO_GENERATOR[slug]
        for qdict in gen():
            yield slug, qdict


def get_bilingual_seed_list() -> list[tuple[str, dict]]:
    return list(iter_bilingual_seed())


def assert_full_bank() -> None:
    rows = get_bilingual_seed_list()
    if len(rows) != 350:
        raise RuntimeError(f"Expected 350 bilingual questions, got {len(rows)}")
    slugs = [s for s, _ in rows]
    for _name_en, slug, _name_ar in BILINGUAL_CATEGORIES:
        c = slugs.count(slug)
        if c != 50:
            raise RuntimeError(f"Expected 50 questions for {slug}, got {c}")
