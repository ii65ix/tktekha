"""50 science questions (EN + matching AR)."""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import shuffle_preserve_pairs

_SCIENCE_RAW: list[tuple[str, str, list[tuple[str, str]], int]] = [
    ("What is the chemical formula of water?", "ما الصيغة الكيميائية للماء؟", [("H₂O", "H₂O"), ("CO₂", "CO₂"), ("NaCl", "NaCl"), ("O₂", "O₂")], 1),
    ("What is the approximate speed of light in vacuum?", "ما السرعة التقريبية للضوء في الفراغ؟", [("About 300,000 km/s", "حوالي 300000 كم/ث"), ("About 340 m/s", "حوالي 340 م/ث"), ("About 1 km/s", "حوالي 1 كم/ث"), ("About 10,000 km/s", "حوالي 10000 كم/ث")], 1),
    ("What does DNA stand for?", "ماذا تعني DNA؟", [("Deoxyribonucleic acid", "حمض الديوكسي ريبونوكليك"), ("Diurnal Natural Atom", "ذرة طبيعية نهارية"), ("Dynamic Neural Array", "مصفوفة عصبية ديناميكية"), ("Dual Nitrogen Acid", "حمض النيتروجين المزدوج")], 1),
    ("What gas do plants mainly release during photosynthesis?", "ما الغاز الذي تطلقه النباتات غالبًا أثناء التمثيل الضوئي؟", [("Oxygen", "الأكسجين"), ("Carbon dioxide", "ثاني أكسيد الكربون"), ("Nitrogen", "النيتروجين"), ("Hydrogen", "الهيدروجين")], 1),
    ("What does Earth's gravity roughly cause near the surface?", "ماذا تسبب جاذبية الأرض تقريبًا قرب السطح؟", [("Objects to accelerate downward at about 9.8 m/s²", "تسارع الأجسام نحو الأسفل بحوالي 9.8 م/ث²"), ("Objects to float upward", "طفو الأجسام لأعلى"), ("Zero acceleration", "تسارع صفر"), ("Light to stop", "توقف الضوء")], 1),
    ("Which planet is famous for its prominent ring system?", "أي كوكب مشهور بحلقاته البارزة؟", [("Saturn", "زحل"), ("Mercury", "عطارد"), ("Venus", "الزهرة"), ("Mars", "المريخ")], 1),
    ("Which planet is the largest in our solar system?", "أي كوكب هو الأكبر في مجموعتنا الشمسية؟", [("Jupiter", "المشتري"), ("Earth", "الأرض"), ("Neptune", "نبتون"), ("Mars", "المريخ")], 1),
    ("What is the atomic number of hydrogen?", "ما العدد الذري للهيدروجين؟", [("1", "1"), ("2", "2"), ("8", "8"), ("10", "10")], 1),
    ("Newton's third law says forces come in what?", "قانون نيوتن الثالث يقول إن القوى تأتي في أي شكل؟", [("Pairs: equal and opposite", "أزواج: متساوية ومتعاكسة"), ("Triples only", "ثلاثيات فقط"), ("Singles only", "مفردة فقط"), ("Circles", "دوائر")], 1),
    ("What pH is considered neutral at 25°C for pure water?", "ما الرقم الهيدروجيني الذي يُعتبر محايدًا عند 25°م للماء النقي؟", [("7", "7"), ("0", "0"), ("14", "14"), ("1", "1")], 1),
    ("What do red blood cells mainly transport?", "ماذا تنقل كريات الدم الحمراء أساسًا؟", [("Oxygen", "الأكسجين"), ("Digestive enzymes", "إنزيمات هضمية"), ("Insulin only", "إنسولين فقط"), ("Vitamin D only", "فيتامين د فقط")], 1),
    ("Which organelle is often called the 'powerhouse' of the cell?", "أي عضية تُسمى غالبًا 'محطة الطاقة' للخلية؟", [("Mitochondria", "الميتوكندريا"), ("Ribosome", "الريبوسوم"), ("Golgi apparatus", "جهاز غولجي"), ("Vacuole", "فجوة")], 1),
    ("What pigment makes many plants look green?", "ما الصبغة التي تجعل كثيرًا من النباتات تبدو خضراء؟", [("Chlorophyll", "الكلوروفيل"), ("Melanin", "الميلانين"), ("Hemoglobin", "الهيموغلوبين"), ("Keratin", "الكيراتين")], 1),
    ("Who is often credited with creating an early periodic table of elements?", "من يُنسب إليه غالبًا إنشاء جدول دوري مبكر للعناصر؟", [("Dmitri Mendeleev", "ديميتري مندليف"), ("Isaac Newton", "إسحاق نيوتن"), ("Charles Darwin", "تشارلز داروين"), ("Marie Curie", "ماري كوري")], 1),
    ("A light-year measures what?", "ما الذي تقيسه السنة الضوئية؟", [("Distance", "مسافة"), ("Time only", "زمن فقط"), ("Mass", "كتلة"), ("Temperature", "حرارة")], 1),
    ("Why do viruses need a host cell?", "لماذا تحتاج الفيروسات إلى خلية مضيفة؟", [("They use the host machinery to replicate", "تستخدم آلية المضيف للتضاعف"), ("They eat metal", "تأكل المعادن"), ("They photosynthesize", "تمارس التمثيل الضوئي"), ("They divide like bacteria always", "تنقسم مثل البكتيريا دائمًا")], 1),
    ("What is absolute zero on the Celsius scale?", "ما الصفر المطلق على مقياس سيلسيوس؟", [("About −273.15°C", "حوالي −273.15°م"), ("0°C", "0°م"), ("−100°C", "−100°م"), ("−500°C", "−500°م")], 1),
    ("What is the chemical symbol for gold?", "ما الرمز الكيميائي للذهب؟", [("Au", "Au"), ("Ag", "Ag"), ("Fe", "Fe"), ("Cu", "Cu")], 1),
    ("What is the chemical symbol for iron?", "ما الرمز الكيميائي للحديد؟", [("Fe", "Fe"), ("Ir", "Ir"), ("I", "I"), ("F", "F")], 1),
    ("What is the usual molecular form of oxygen in air?", "ما الشكل الجزيئي المعتاد للأكسجين في الهواء؟", [("O₂", "O₂"), ("O", "O"), ("O₃ only in air", "O₃ فقط في الهواء"), ("H₂O", "H₂O")], 1),
    ("What is the formula of carbon dioxide?", "ما صيغة ثاني أكسيد الكربون؟", [("CO₂", "CO₂"), ("CO", "CO"), ("C₂O", "C₂O"), ("O₂", "O₂")], 1),
    ("Dry air is mostly which gas by volume?", "الهواء الجاف غالبًا أي غاز حسب الحجم؟", [("Nitrogen", "النيتروجين"), ("Oxygen", "الأكسجين"), ("Carbon dioxide", "ثاني أكسيد الكربون"), ("Helium", "الهيليوم")], 1),
    ("What does the Moon mainly orbit?", "ما الذي يدور حوله القمر أساسًا؟", [("Earth", "الأرض"), ("The Sun", "الشمس"), ("Mars", "المريخ"), ("Jupiter", "المشتري")], 1),
    ("Where does photosynthesis mainly occur in plant cells?", "أين يحدث التمثيل الضوئي غالبًا في خلايا النبات؟", [("Chloroplasts", "البَلَسْتيدات الخضراء"), ("Mitochondria only", "الميتوكندريا فقط"), ("Nucleus", "النواة"), ("Cell wall only", "الجدار الخلوي فقط")], 1),
    ("Where does chemical digestion of starch begin in humans?", "أين يبدأ الهضم الكيميائي للنشاء عند الإنسان؟", [("Mouth (saliva)", "الفم (اللعاب)"), ("Stomach only", "المعدة فقط"), ("Large intestine", "القولون"), ("Liver", "الكبد")], 1),
    ("How many chambers does a human heart have?", "كم أذينة وبطينة لقلب الإنسان؟", [("4", "4"), ("2", "2"), ("3", "3"), ("5", "5")], 1),
    ("What is the largest part of the human brain by volume?", "ما أكبر جزء من دماغ الإنسان حجمًا؟", [("Cerebrum", "المخ"), ("Cerebellum", "المخيخ"), ("Medulla only", "التمدد فقط"), ("Spinal cord", "الحبل الشوكي")], 1),
    ("Newton's first law is also called the law of what?", "قانون نيوتن الأول يُسمى أيضًا قانون ماذا؟", [("Inertia", "القصور الذاتي"), ("Gravity", "الجاذبية"), ("Friction", "الاحتكاك"), ("Entropy", "الإنتروبيا")], 1),
    ("What kind of energy does a moving object have?", "ما نوع الطاقة للجسم المتحرك؟", [("Kinetic energy", "طاقة حركية"), ("Potential energy only", "طاقة وضع فقط"), ("Chemical energy in all cases", "طاقة كيميائية في كل الحالات"), ("Nuclear energy always", "طاقة نووية دائمًا")], 1),
    ("What energy is stored due to position or state (e.g., height)?", "ما الطاقة المخزنة بسبب الوضع أو الحالة (مثل الارتفاع)؟", [("Potential energy", "طاقة وضع"), ("Kinetic only", "حركية فقط"), ("Thermal only", "حرارية فقط"), ("Sound only", "صوتية فقط")], 1),
    ("What surrounds a typical animal cell and controls what enters?", "ما الذي يحيط بالخلية الحيوانية النموذجية ويتحكم بالدخول؟", [("Cell membrane", "الغشاء البلازمي"), ("Cell wall (typical animal)", "جدار خلوي (حيواني نموذجي)"), ("Chloroplast", "بلاستيدة خضراء"), ("Ribosome only", "ريبوسوم فقط")], 1),
    ("Where is most of a cell's DNA kept in eukaryotes?", "أين يُحفظ معظم DNA في حقيقيات النواة؟", [("Nucleus", "النواة"), ("Mitochondria only", "الميتوكندريا فقط"), ("Cytoplasm only", "السيتوبلازم فقط"), ("Cell membrane", "الغشاء البلازمي")], 1),
    ("What makes proteins in the cell?", "ما الذي يصنع البروتينات في الخلية؟", [("Ribosomes", "الريبوسومات"), ("Lysosomes only", "الحُلَيْميات فقط"), ("Vacuoles only", "الفجوات فقط"), ("Nucleolus only", "النوية فقط")], 1),
    ("What is an ecosystem?", "ما النظام البيئي؟", [("Living organisms interacting with their environment", "كائنات حية تتفاعل مع بيئتها"), ("Only rocks", "صخور فقط"), ("Only weather", "طقس فقط"), ("Only one species isolated", "نوع واحد معزول")], 1),
    ("In a simple food chain, plants are often what?", "في سلسلة غذائية بسيطة، النباتات غالبًا ماذا؟", [("Producers", "منتجون"), ("Top carnivores", "لواحم قمة"), ("Decomposers only", "محللات فقط"), ("Omnivores always", "آكلة للكل دائمًا")], 1),
    ("What is evaporation?", "ما التبخر؟", [("Liquid turning into gas at the surface", "تحول السائل إلى غاز من السطح"), ("Gas turning to liquid", "غاز يصبح سائلًا"), ("Solid to liquid only", "صلب إلى سائل فقط"), ("Liquid to solid", "سائل إلى صلب")], 1),
    ("What is condensation?", "ما التكثف؟", [("Gas turning into liquid", "تحول الغاز إلى سائل"), ("Liquid to gas", "سائل إلى غاز"), ("Solid to gas directly", "صلب إلى غاز مباشرة"), ("Liquid to solid", "سائل إلى صلب")], 1),
    ("At standard pressure, what is the boiling point of pure water (sea level)?", "عند الضغط المعياري، ما نقطة غليان الماء النقي (مستوى سطح البحر)؟", [("100°C", "100°م"), ("0°C", "0°م"), ("50°C", "50°م"), ("212°C", "212°م")], 1),
    ("Density is mass divided by what?", "الكثافة كتلة مقسومة على ماذا؟", [("Volume", "الحجم"), ("Time", "الزمن"), ("Speed", "السرعة"), ("Force", "القوة")], 1),
    ("What force resists motion between surfaces in contact?", "ما القوة التي تقاوم الحركة بين الأسطح المتلامسة؟", [("Friction", "الاحتكاك"), ("Lift", "الرفع"), ("Buoyancy always upward in air", "طفو دائمًا لأعلى في الهواء"), ("Magnetic north only", "القطب الشمالي المغناطيسي فقط")], 1),
    ("How many planets are in our solar system (common modern definition)?", "كم كوكبًا في مجموعتنا الشمسية (تعريف حديث شائع)؟", [("8", "8"), ("9", "9"), ("7", "7"), ("10", "10")], 1),
    ("Which planet is closest to the Sun?", "أي كوكب الأقرب إلى الشمس؟", [("Mercury", "عطارد"), ("Venus", "الزهرة"), ("Earth", "الأرض"), ("Mars", "المريخ")], 1),
    ("Which planet is usually the farthest from the Sun among these?", "أي كوكب عادةً الأبعد عن الشمس بين هذه؟", [("Neptune", "نبتون"), ("Uranus", "أورانوس"), ("Saturn", "زحل"), ("Jupiter", "المشتري")], 1),
    ("How many moons does Earth have (commonly counted)?", "كم قمرًا للأرض (عدّ شائع)؟", [("1", "1"), ("2", "2"), ("0", "0"), ("3", "3")], 1),
    ("Earth's seasons are mainly caused by what?", "فصول الأرض سببها أساسًا ماذا؟", [("Axial tilt relative to orbit", "ميل المحور بالنسبة للمدار"), ("Distance to the Sun only", "البعد عن الشمس فقط"), ("Moon phases", "أطوار القمر"), ("Ocean tides only", "المد والجزر فقط")], 1),
    ("What shape is DNA often described as?", "ما الشكل الذي يُوصف به الحمض النووي غالبًا؟", [("Double helix", "لولب مزدوج"), ("Single line", "خط واحد"), ("Cube", "مكعب"), ("Flat circle", "دائرة مسطحة")], 1),
    ("What particle has a negative charge in an atom?", "ما الجسيم ذو الشحنة السالبة في الذرة؟", [("Electron", "إلكترون"), ("Proton", "بروتون"), ("Neutron", "نيوترون"), ("Nucleus whole", "النواة كاملة")], 1),
    ("What particle is in the nucleus and has a positive charge?", "ما الجسيم في النواة وبشحنة موجبة؟", [("Proton", "بروتون"), ("Electron", "إلكترون"), ("Photon", "فوتون"), ("Neutron", "نيوترون")], 1),
    ("What is a neutron's electric charge?", "ما شحنة النيوترون الكهربائية؟", [("Neutral (0)", "متعادلة (0)"), ("+1", "+1"), ("−1", "−1"), ("+2", "+2")], 1),
    ("What force keeps planets in orbit around the Sun?", "ما القوة التي تبقي الكواكب في مدارها حول الشمس؟", [("Gravity", "الجاذبية"), ("Magnetism only", "المغناطيسية فقط"), ("Friction with space", "احتكاك مع الفضاء"), ("Electric charge of air", "شحنة الهواء الكهربائية")], 1),
]


def generate_science(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(46)
    return [shuffle_preserve_pairs(qe, qa, opts, c, rng) for qe, qa, opts, c in _SCIENCE_RAW]
