"""Gateway challenge: تماسيح عبودكا (EN + matching AR).

General knowledge (main), plus programming, technology, and some Islamic
religious questions — bilingual pairs.
"""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import shuffle_preserve_pairs

_TAMASIHA_RAW: list[tuple[str, str, list[tuple[str, str]], int]] = [
    # General (simple / medium)
    (
        "Who wrote the play ‘Romeo and Juliet’?",
        "من كتب مسرحية «روميو وجولييت»؟",
        [
            ("William Shakespeare", "ويليام شكسبير"),
            ("Charles Dickens", "تشارلز ديكنز"),
            ("Mark Twain", "مارك توين"),
            ("Jane Austen", "جين أوستن"),
        ],
        1,
    ),
    (
        "At sea level, pure water boils at about:",
        "عند مستوى سطح البحر، يغلي الماء النقي عند حوالي:",
        [
            ("100 °C", "100 °م"),
            ("0 °C", "0 °م"),
            ("50 °C", "50 °م"),
            ("212 °C", "212 °م"),
        ],
        1,
    ),
    (
        "How many continents are there on Earth (common model)?",
        "كم عدد القارات على الأرض (النموذج الشائع)؟",
        [
            ("7", "7"),
            ("5", "5"),
            ("6", "6"),
            ("8", "8"),
        ],
        1,
    ),
    (
        "What is the capital of Kuwait?",
        "ما عاصمة دولة الكويت؟",
        [
            ("Kuwait City", "مدينة الكويت"),
            ("Basra", "البصرة"),
            ("Riyadh", "الرياض"),
            ("Doha", "الدوحة"),
        ],
        1,
    ),
    (
        "What is the currency of Kuwait?",
        "ما عملة دولة الكويت؟",
        [
            ("Kuwaiti dinar", "الدينار الكويتي"),
            ("Saudi riyal", "الريال السعودي"),
            ("Qatari riyal", "الريال القطري"),
            ("UAE dirham", "الدرهم الإماراتي"),
        ],
        1,
    ),
    (
        "Kuwait is located on which continent (geographically)?",
        "تقع الكويت في أي قارة جغرافيًا؟",
        [
            ("Asia", "آسيا"),
            ("Europe", "أوروبا"),
            ("Africa", "أفريقيا"),
            ("South America", "أمريكا الجنوبية"),
        ],
        1,
    ),
    (
        "Which landmark is famously associated with Kuwait?",
        "أي معلم يرتبط بالكويت بشكل مشهور؟",
        [
            ("Kuwait Towers", "أبراج الكويت"),
            ("Eiffel Tower", "برج إيفل"),
            ("Colosseum", "الكولوسيوم"),
            ("Statue of Liberty", "تمثال الحرية"),
        ],
        1,
    ),
    (
        "Binary uses which number system base?",
        "النظام الثنائي يعتمد على أساس أي رقم؟",
        [
            ("Base 2", "الأساس 2"),
            ("Base 10", "الأساس 10"),
            ("Base 8", "الأساس 8"),
            ("Base 16", "الأساس 16"),
        ],
        1,
    ),
    (
        "What is the largest ocean on Earth?",
        "ما أكبر محيط على الأرض؟",
        [
            ("Pacific Ocean", "المحيط الهادئ"),
            ("Atlantic Ocean", "المحيط الأطلسي"),
            ("Indian Ocean", "المحيط الهندي"),
            ("Arctic Ocean", "المحيط المتجمد الشمالي"),
        ],
        1,
    ),
    (
        "In a leap year, how many days are in February?",
        "في السنة الكبيسة، كم يومًا في شهر فبراير؟",
        [
            ("29", "29"),
            ("28", "28"),
            ("30", "30"),
            ("31", "31"),
        ],
        1,
    ),
    # Medium
    (
        "Which math formula gives the area of a circle?",
        "أي صيغة تعطي مساحة الدائرة؟",
        [
            ("π r²", "π r²"),
            ("2π r", "2π r"),
            ("π d", "π d"),
            ("r/π", "r/π"),
        ],
        1,
    ),
    (
        "In a right triangle, the Pythagorean theorem says:",
        "في المثلث القائم، قانون فيثاغورس يقول:",
        [
            ("a² + b² = c²", "أ² + ب² = ج²"),
            ("a + b = c", "أ + ب = ج"),
            ("a² - b² = c²", "أ² - ب² = ج²"),
            ("c = a/b", "ج = أ/ب"),
        ],
        1,
    ),
    (
        "What does HTML stand for?",
        "ماذا تعني اختصار HTML؟",
        [
            ("HyperText Markup Language", "لغة ترميز النص التشعبي"),
            ("High Transfer Multi Layout", "تنسيق متعدد عالي النقل"),
            ("Home Tool Meta Link", "أداة منزلية وروابط"),
            ("HyperText Message Language", "لغة رسائل نص تشعبي"),
        ],
        1,
    ),
    (
        "Which HTTP method is typically used to send data from an HTML form?",
        "أي طريقة HTTP تُستخدم عادةً لإرسال بيانات نموذج HTML؟",
        [
            ("POST", "POST"),
            ("GET", "GET"),
            ("PUT", "PUT"),
            ("TRACE", "TRACE"),
        ],
        1,
    ),
    (
        "During photosynthesis, plants mainly take in which gas from the air?",
        "أثناء التمثيل الضوئي، ما الغاز الذي تمتصه النباتات أساسًا من الهواء؟",
        [
            ("Carbon dioxide (CO₂)", "ثاني أكسيد الكربون (CO₂)"),
            ("Oxygen (O₂)", "الأكسجين (O₂)"),
            ("Nitrogen (N₂)", "النيتروجين (N₂)"),
            ("Hydrogen (H₂)", "الهيدروجين (H₂)"),
        ],
        1,
    ),
    (
        "What is the largest planet in our solar system?",
        "ما أكبر كوكب في مجموعتنا الشمسية؟",
        [
            ("Jupiter", "المشتري"),
            ("Saturn", "زحل"),
            ("Earth", "الأرض"),
            ("Neptune", "نبتون"),
        ],
        1,
    ),
    (
        "What does API commonly stand for in software?",
        "ماذا يعني اختصار API في البرمجيات غالبًا؟",
        [
            (
                "Application Programming Interface",
                "واجهة برمجة التطبيقات",
            ),
            ("Automatic Program Installation", "تثبيت برامج تلقائي"),
            ("Advanced Process Index", "فهرس عمليات متقدم"),
            ("App Performance Indicator", "مؤشر أداء التطبيق"),
        ],
        1,
    ),
    (
        "Which layer of Earth’s atmosphere contains the ozone layer that helps block UV?",
        "أي طبقة من الغلاف الجوي للأرض تحتوي على طبقة الأوزون التي تساعد على حجب الأشعة فوق البنفسجية؟",
        [
            ("Stratosphere", "الستراتوسفير"),
            ("Troposphere", "التروبوسفير"),
            ("Mesosphere", "الميزوسفير"),
            ("Thermosphere", "الثرموسفير"),
        ],
        1,
    ),
    (
        "The human genetic material DNA is most famously described as:",
        "المادة الوراثية لدى الإنسان (DNA) تُوصف غالبًا بأنها:",
        [
            ("A double helix", "لولب مزدوج"),
            ("A single straight chain", "سلسلة مستقيمة واحدة"),
            ("A cube lattice", "شبكة مكعبات"),
            ("Only proteins", "بروتينات فقط"),
        ],
        1,
    ),
    (
        "World War II in Europe is commonly considered to have ended in Europe in:",
        "يُعتبر أن الحرب العالمية الثانية انتهت في أوروبا غالبًا في:",
        [
            ("1945", "1945"),
            ("1918", "1918"),
            ("1939", "1939"),
            ("1950", "1950"),
        ],
        1,
    ),
    # Hard
    (
        "What is the capital city of Australia?",
        "ما عاصمة أستراليا؟",
        [
            ("Canberra", "كانبيرا"),
            ("Sydney", "سيدني"),
            ("Melbourne", "ملبورن"),
            ("Brisbane", "بريزبن"),
        ],
        1,
    ),
    (
        "What is the chemical symbol for gold?",
        "ما الرمز الكيميائي للذهب؟",
        [
            ("Au", "Au"),
            ("Ag", "Ag"),
            ("Go", "Go"),
            ("Gd", "Gd"),
        ],
        1,
    ),
    # Programming / tech
    (
        "In a typical program, what is a `for` loop mainly used for?",
        "في البرمجة، ما الغرض الرئيسي من حلقة `for`؟",
        [
            ("Repeating a block of code multiple times", "تكرار تعليمات عدة مرات"),
            ("Deleting files permanently", "حذف الملفات نهائيًا"),
            ("Drawing only graphics", "رسم رسومات فقط"),
            ("Stopping the internet", "إيقاف الإنترنت"),
        ],
        1,
    ),
    (
        "In programming, a variable is best described as:",
        "في البرمجة، يُوصف المتغير غالبًا بأنه:",
        [
            ("A named place to store a value", "اسم لمكان يحفظ قيمة"),
            ("A type of computer virus", "نوع من فيروسات الحاسوب"),
            ("Only a keyboard shortcut", "اختصار لوحة مفاتيح فقط"),
            ("A monitor screen size", "حجم الشاشة"),
        ],
        1,
    ),
    (
        "What does CPU stand for?",
        "ماذا تعني اختصار CPU؟",
        [
            ("Central Processing Unit", "وحدة المعالجة المركزية"),
            ("Computer Power Unit", "وحدة طاقة الحاسوب"),
            ("Core Processing Utility", "أداة معالجة أساسية"),
            ("Central Print Utility", "أداة طباعة مركزية"),
        ],
        1,
    ),
    (
        "RAM is usually used for:",
        "الذاكرة العشوائية (RAM) تُستخدم عادةً لـ:",
        [
            ("Temporary fast storage while programs run", "تخزين مؤقت سريع أثناء تشغيل البرامج"),
            ("Permanent file storage after shutdown", "تخزين دائم للملفات بعد الإيقاف"),
            ("Only cooling the CPU", "تبريد المعالج فقط"),
            ("Only display brightness", "سطوع الشاشة فقط"),
        ],
        1,
    ),
    (
        "Wi‑Fi is a technology mainly for:",
        "تقنية Wi‑Fi تُستخدم أساسًا من أجل:",
        [
            ("Wireless networking over radio waves", "شبكة لاسلكية عبر موجات راديوية"),
            ("Wired only connections", "اتصالات سلكية فقط"),
            ("Printing only", "الطباعة فقط"),
            ("CPU cooling", "تبريد المعالج"),
        ],
        1,
    ),
    (
        "Which device is best described as an ‘input’ device?",
        "أي جهاز يُعدّ من أجهزة الإدخال؟",
        [
            ("Keyboard", "لوحة المفاتيح"),
            ("Monitor", "الشاشة"),
            ("Speaker", "مكبّر الصوت"),
            ("Printer", "الطابعة"),
        ],
        1,
    ),
    # Islamic (religious)
    (
        "How many pillars of Islam are there?",
        "كم عدد أركان الإسلام؟",
        [
            ("5", "5"),
            ("4", "4"),
            ("6", "6"),
            ("7", "7"),
        ],
        1,
    ),
    (
        "In the Islamic calendar, Ramadan is which month?",
        "في التقويم الهجري، رمضان هو أي شهر؟",
        [
            ("The 9th month", "الشهر التاسع"),
            ("The 1st month", "الشهر الأول"),
            ("The 12th month", "الشهر الثاني عشر"),
            ("The 6th month", "الشهر السادس"),
        ],
        1,
    ),
    (
        "Muslims face which direction for prayer (Salah)?",
        "تجاه أي اتجاه يصلي المسلمون في الصلاة؟",
        [
            ("Toward the Kaaba in Makkah", "نحو الكعبة في مكة"),
            ("Toward the east only", "نحو الشرق فقط"),
            ("Toward the north only", "نحو الشمال فقط"),
            ("Any random direction", "أي اتجاه عشوائي"),
        ],
        1,
    ),
    (
        "The first Quranic revelation to Prophet Muhammad ﷺ is linked to which place?",
        "أول نزول من القرآن على النبي محمد ﷺ يرتبط بأي مكان؟",
        [
            ("Cave Hira on Jabal al-Nour", "غار حراء على جبل النور"),
            ("The Kaaba courtyard", "ساحة الكعبة"),
            ("Mount Uhud", "جبل أحد"),
            ("Al-Aqsa Mosque", "المسجد الأقصى"),
        ],
        1,
    ),
    (
        "How many obligatory (Fard) daily prayers are there in Islam?",
        "كم عدد الصلوات الفرض اليومية في الإسلام؟",
        [
            ("5", "5"),
            ("3", "3"),
            ("4", "4"),
            ("7", "7"),
        ],
        1,
    ),
    (
        "What is Zakah in Islam?",
        "ما هي الزكاة في الإسلام؟",
        [
            ("An obligatory charity on qualifying wealth", "صدقة واجبة على أموال مؤهلة"),
            ("Only optional tips", "بخشيش اختياري فقط"),
            ("Only fasting", "صيام فقط"),
            ("Only Hajj", "حج فقط"),
        ],
        1,
    ),
]


def generate_tamasih_abudka(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(48)
    return [shuffle_preserve_pairs(qe, qa, opts, c, rng) for qe, qa, opts, c in _TAMASIHA_RAW]
