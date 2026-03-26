"""50 geography questions — capitals & countries (EN + matching AR)."""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import pick_three_wrong, shuffle_preserve_pairs

# (country EN, country AR, capital EN, capital AR)
GEO_ROWS: list[tuple[str, str, str, str]] = [
    ("France", "فرنسا", "Paris", "باريس"),
    ("Germany", "ألمانيا", "Berlin", "برلين"),
    ("Italy", "إيطاليا", "Rome", "روما"),
    ("Spain", "إسبانيا", "Madrid", "مدريد"),
    ("United Kingdom", "المملكة المتحدة", "London", "لندن"),
    ("Japan", "اليابان", "Tokyo", "طوكيو"),
    ("China", "الصين", "Beijing", "بكين"),
    ("Brazil", "البرازيل", "Brasília", "برازيليا"),
    ("Egypt", "مصر", "Cairo", "القاهرة"),
    ("Saudi Arabia", "المملكة العربية السعودية", "Riyadh", "الرياض"),
    ("United Arab Emirates", "الإمارات العربية المتحدة", "Abu Dhabi", "أبوظبي"),
    ("Morocco", "المغرب", "Rabat", "الرباط"),
    ("Algeria", "الجزائر", "Algiers", "الجزائر"),
    ("Tunisia", "تونس", "Tunis", "تونس"),
    ("Jordan", "الأردن", "Amman", "عمّان"),
    ("Lebanon", "لبنان", "Beirut", "بيروت"),
    ("Iraq", "العراق", "Baghdad", "بغداد"),
    ("Kuwait", "الكويت", "Kuwait City", "مدينة الكويت"),
    ("Qatar", "قطر", "Doha", "الدوحة"),
    ("Oman", "عُمان", "Muscat", "مسقط"),
    ("United States", "الولايات المتحدة", "Washington, D.C.", "واشنطن"),
    ("Canada", "كندا", "Ottawa", "أوتاوا"),
    ("Mexico", "المكسيك", "Mexico City", "مدينة المكسيك"),
    ("Argentina", "الأرجنتين", "Buenos Aires", "بوينس آيرس"),
    ("Australia", "أستراليا", "Canberra", "كانبرا"),
    ("India", "الهند", "New Delhi", "نيودلهي"),
    ("Pakistan", "باكستان", "Islamabad", "إسلام أباد"),
    ("Indonesia", "إندونيسيا", "Jakarta", "جاكرتا"),
    ("Malaysia", "ماليزيا", "Kuala Lumpur", "كوالالمبور"),
    ("Thailand", "تايلاند", "Bangkok", "بانكوك"),
    ("South Korea", "كوريا الجنوبية", "Seoul", "سيول"),
    ("Russia", "روسيا", "Moscow", "موسكو"),
    ("Turkey", "تركيا", "Ankara", "أنقرة"),
    ("Greece", "اليونان", "Athens", "أثينا"),
    ("Portugal", "البرتغال", "Lisbon", "لشبونة"),
    ("Netherlands", "هولندا", "Amsterdam", "أمستردام"),
    ("Belgium", "بلجيكا", "Brussels", "بروكسل"),
    ("Switzerland", "سويسرا", "Bern", "برن"),
    ("Austria", "النمسا", "Vienna", "فيينا"),
    ("Sweden", "السويد", "Stockholm", "ستوكهولم"),
    ("Norway", "النرويج", "Oslo", "أوسلو"),
    ("Denmark", "الدنمارك", "Copenhagen", "كوبنهاغن"),
    ("Finland", "فنلندا", "Helsinki", "هلسنكي"),
    ("Poland", "بولندا", "Warsaw", "وارسو"),
    ("Nigeria", "نيجيريا", "Abuja", "أبوجا"),
    ("Kenya", "كينيا", "Nairobi", "نيروبي"),
    ("South Africa", "جنوب أفريقيا", "Pretoria", "بريتوريا"),
    ("Colombia", "كولومبيا", "Bogotá", "بوغوتا"),
    ("Chile", "تشيلي", "Santiago", "سانتياغو"),
    ("Venezuela", "فنزويلا", "Caracas", "كراكاس"),
]


def generate_geography(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(42)
    capitals = [(row[2], row[3]) for row in GEO_ROWS]
    out: list[dict] = []
    for country_en, country_ar, cap_en, cap_ar in GEO_ROWS:
        correct_pair = (cap_en, cap_ar)
        wrong = pick_three_wrong(capitals, correct_pair, rng)
        opts = [correct_pair] + wrong
        q_en = f"What is the capital of {country_en}?"
        q_ar = f"ما عاصمة {country_ar}؟"
        out.append(shuffle_preserve_pairs(q_en, q_ar, opts, 1, rng))
    return out
