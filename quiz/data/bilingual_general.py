"""50 general knowledge questions (EN + matching AR)."""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import shuffle_preserve_pairs

_GENERAL_RAW: list[tuple[str, str, list[tuple[str, str]], int]] = [
    ("What is the chemical symbol for water?", "ما الرمز الكيميائي للماء؟", [("H2O", "H2O"), ("CO2", "CO2"), ("O2", "O2"), ("NaCl", "NaCl")], 1),
    ("Who painted the Mona Lisa?", "من رسم الموناليزا؟", [("Leonardo da Vinci", "ليوناردو دا فينشي"), ("Michelangelo", "مايكل أنجلو"), ("Van Gogh", "فان غوخ"), ("Picasso", "بيكاسو")], 1),
    ("What is the largest planet in our solar system?", "ما أكبر كوكب في مجموعتنا الشمسية؟", [("Jupiter", "المشتري"), ("Saturn", "زحل"), ("Earth", "الأرض"), ("Neptune", "نبتون")], 1),
    ("How many continents are there?", "كم قارة في العالم؟", [("7", "7"), ("5", "5"), ("6", "6"), ("8", "8")], 1),
    ("What is the hardest natural substance on Earth?", "ما أصلب مادة طبيعية على الأرض؟", [("Diamond", "الماس"), ("Gold", "الذهب"), ("Iron", "الحديد"), ("Quartz", "الكوارتز")], 1),
    ("Which gas do plants absorb from the air?", "ما الغاز الذي تمتصه النباتات من الهواء؟", [("Carbon dioxide", "ثاني أكسيد الكربون"), ("Oxygen", "الأكسجين"), ("Nitrogen", "النيتروجين"), ("Helium", "الهيليوم")], 1),
    ("What is the capital of Japan?", "ما عاصمة اليابان؟", [("Tokyo", "طوكيو"), ("Kyoto", "كيوتو"), ("Osaka", "أوساكا"), ("Hiroshima", "هيروشيما")], 1),
    ("Who wrote 'Romeo and Juliet'?", "من كتب روميو وجولييت؟", [("William Shakespeare", "ويليام شكسبير"), ("Charles Dickens", "تشارلز ديكنز"), ("Jane Austen", "جين أوستن"), ("Homer", "هوميروس")], 1),
    ("What is the speed of light approximately?", "ما سرعة الضوء تقريبًا؟", [("300,000 km/s", "300000 كم/ث"), ("150,000 km/s", "150000 كم/ث"), ("1,000 km/s", "1000 كم/ث"), ("30,000 km/s", "30000 كم/ث")], 1),
    ("Which ocean is the largest?", "ما أكبر محيط؟", [("Pacific", "الهادئ"), ("Atlantic", "الأطلسي"), ("Indian", "الهندي"), ("Arctic", "المتجمد الشمالي")], 1),
    ("What is the smallest prime number?", "ما أصغر عدد أولي؟", [("2", "2"), ("0", "0"), ("1", "1"), ("3", "3")], 1),
    ("In which year did World War II end?", "في أي انتهت الحرب العالمية الثانية؟", [("1945", "1945"), ("1944", "1944"), ("1939", "1939"), ("1950", "1950")], 1),
    ("What is the main language of Brazil?", "ما اللغة الرئيسية في البرازيل؟", [("Portuguese", "البرتغالية"), ("Spanish", "الإسبانية"), ("English", "الإنجليزية"), ("French", "الفرنسية")], 1),
    ("What is the currency of the United Kingdom?", "ما عملة المملكة المتحدة؟", [("Pound sterling", "الجنيه الإسترليني"), ("Euro", "اليورو"), ("Dollar", "الدولار"), ("Franc", "الفرنك")], 1),
    ("Which vitamin is produced when skin is exposed to sunlight?", "ما الفيتامين الذي يُنتج عند تعرض الجلد لأشعة الشمس؟", [("Vitamin D", "فيتامين د"), ("Vitamin C", "فيتامين ج"), ("Vitamin A", "فيتامين أ"), ("Vitamin B12", "فيتامين ب12")], 1),
    ("What is the largest mammal in the world?", "ما أكبر ثديي في العالم؟", [("Blue whale", "الحوت الأزرق"), ("Elephant", "الفيل"), ("Giraffe", "الزرافة"), ("Hippo", "فرس النهر")], 1),
    ("Which country invented paper?", "أي بلد اخترع الورق؟", [("China", "الصين"), ("Egypt", "مصر"), ("India", "الهند"), ("Greece", "اليونان")], 1),
    ("What is the powerhouse of the cell?", "ما محطة الطاقة في الخلية؟", [("Mitochondria", "الميتوكوندريا"), ("Nucleus", "النواة"), ("Ribosome", "الريبوسوم"), ("Chloroplast", "البلاستيدة الخضراء")], 1),
    ("What does DNA stand for?", "ماذا تعني DNA؟", [("Deoxyribonucleic acid", "حمض الديوكسي ريبونوكليك"), ("Dynamic nucleic acid", "حمض نووي ديناميكي"), ("Dual nuclear acid", "حمض نووي مزدوج"), ("Diacid nucleic acid", "حمض نووي ثنائي")], 1),
    ("Which planet is known as the Red Planet?", "ما الكوكب المعروف بالكوكب الأحمر؟", [("Mars", "المريخ"), ("Venus", "الزهرة"), ("Jupiter", "المشتري"), ("Mercury", "عطارد")], 1),
    ("What is the boiling point of water at sea level (°C)?", "ما نقطة غليان الماء عند مستوى سطح البحر (°م)؟", [("100", "100"), ("90", "90"), ("80", "80"), ("120", "120")], 1),
    ("Who discovered gravity (classical story)?", "من اكتشف الجاذبية (القصة الكلاسيكية)؟", [("Isaac Newton", "إسحاق نيوتن"), ("Albert Einstein", "ألبرت أينشتاين"), ("Galileo Galilei", "غاليليو غاليلي"), ("Nikola Tesla", "نيكولا تسلا")], 1),
    ("What is the largest desert in the world?", "ما أكبر صحراء في العالم؟", [("Antarctic (polar desert)", "أنتاركتيكا (صحراء قطبية)"), ("Sahara", "الصحراء الكبرى"), ("Gobi", "جوبي"), ("Arabian", "الصحراء العربية")], 1),
    ("How many bones in an adult human body (typical)?", "كم عظمة في جسم البالغ تقريبًا؟", [("206", "206"), ("180", "180"), ("250", "250"), ("300", "300")], 1),
    ("What is the nearest star to Earth?", "ما أقرب نجم إلى الأرض؟", [("The Sun", "الشمس"), ("Proxima Centauri", "بروكسيما قنطورس"), ("Sirius", "سيريوس"), ("Polaris", "القطب")], 1),
    ("Which festival of lights is widely celebrated in India?", "أي مهرجان أضواء يُحتفل به على نطاق واسع في الهند؟", [("Diwali", "ديوالي"), ("Hanukkah", "الحانوكا"), ("Christmas", "عيد الميلاد"), ("Eid", "العيد")], 1),
    ("What is the main gas in Earth’s atmosphere?", "ما الغاز الرئيسي في الغلاف الجوي للأرض؟", [("Nitrogen", "النيتروجين"), ("Oxygen", "الأكسجين"), ("Carbon dioxide", "ثاني أكسيد الكربون"), ("Argon", "الأرغون")], 1),
    ("What is the pH of pure water?", "ما الرقم الهيدروجيني للماء النقي؟", [("7", "7"), ("0", "0"), ("14", "14"), ("1", "1")], 1),
    ("Which organ pumps blood through the body?", "ما العضو الذي يضخ الدم في الجسم؟", [("Heart", "القلب"), ("Liver", "الكبد"), ("Lung", "الرئة"), ("Kidney", "الكلية")], 1),
    ("What is the tallest mountain above sea level?", "ما أعلى جبل فوق مستوى سطح البحر؟", [("Mount Everest", "إيفرست"), ("K2", "كي2"), ("Kilimanjaro", "كليمنجارو"), ("Denali", "دينالي")], 1),
    ("Which country has the largest population (approx. recent)?", "أي دولة أكبر عدد سكان (تقريبًا)؟", [("India", "الهند"), ("China", "الصين"), ("USA", "الولايات المتحدة"), ("Indonesia", "إندونيسيا")], 1),
    ("What is the freezing point of water (°C)?", "ما نقطة تجميد الماء (°م)؟", [("0", "0"), ("100", "100"), ("32", "32"), ("−1", "−1")], 1),
    ("Who is known for the theory of relativity?", "من يُعرف بنظرية النسبية؟", [("Albert Einstein", "ألبرت أينشتاين"), ("Isaac Newton", "إسحاق نيوتن"), ("Stephen Hawking", "ستيفن هوكينغ"), ("Marie Curie", "ماري كوري")], 1),
    ("What is the largest island in the world?", "ما أكبر جزيرة في العالم؟", [("Greenland", "غرينلاند"), ("New Guinea", "غينيا الجديدة"), ("Borneo", "بورنيو"), ("Madagascar", "مدغشقر")], 1),
    ("Which metal is liquid at room temperature?", "ما المعدن السائل عند درجة حرارة الغرفة؟", [("Mercury", "الزئبق"), ("Iron", "الحديد"), ("Gold", "الذهب"), ("Aluminum", "الألومنيوم")], 1),
    ("What is the chemical symbol for gold?", "ما الرمز الكيميائي للذهب؟", [("Au", "Au"), ("Ag", "Ag"), ("Go", "Go"), ("Gd", "Gd")], 1),
    ("Which ancient wonder was a lighthouse in Alexandria?", "أي عجيبة قديمة كانت منارة في الإسكندرية؟", [("Lighthouse of Alexandria", "منارة الإسكندرية"), ("Colossus of Rhodes", "عملاق رودس"), ("Hanging Gardens", "الحدائق المعلقة"), ("Pyramid of Giza", "هرم الجيزة")], 1),
    ("What is the largest living structure on Earth (often cited)?", "ما أكبر كائن حي على الأرض (غالبًا)؟", [("Great Barrier Reef", "الحاجز المرجاني العظيم"), ("Blue whale", "الحوت الأزرق"), ("Amazon rainforest", "غابة الأمازون"), ("Giant sequoia tree", "شجرة السكويا العملاقة")], 1),
    ("What is the capital of Canada?", "ما عاصمة كندا؟", [("Ottawa", "أوتاوا"), ("Toronto", "تورنتو"), ("Vancouver", "فانكوفر"), ("Montreal", "مونتريال")], 1),
    ("Which gas do humans exhale most (by volume in breath)?", "ما الغاز الذي يزفره الإنسان أكثر (حجمًا)؟", [("Carbon dioxide", "ثاني أكسيد الكربون"), ("Oxygen", "الأكسجين"), ("Nitrogen", "النيتروجين"), ("Hydrogen", "الهيدروجين")], 1),
    ("What is the study of fossils called?", "ما اسم دراسة المستحاثات؟", [("Paleontology", "علم المستحاثات"), ("Geology", "الجيولوجيا"), ("Archaeology", "الآثار"), ("Biology", "الأحياء")], 1),
    ("Which blood type is often called universal donor (red cells)?", "ما فصيلة الدم التي تُسمى متبرعًا عامًا (كريات)؟", [("O negative", "O سالب"), ("AB positive", "AB موجب"), ("A positive", "A موجب"), ("B negative", "B سالب")], 1),
    ("What is the center of an atom called?", "ما مركز الذرة؟", [("Nucleus", "النواة"), ("Electron shell", "غلاف الإلكترون"), ("Neutron cloud", "سحابة النيوترون"), ("Proton ring", "حلقة البروتون")], 1),
    ("Which country is famous for the pyramids of Giza?", "أي بلد مشهر بأهرامات الجيزة؟", [("Egypt", "مصر"), ("Mexico", "المكسيك"), ("Sudan", "السودان"), ("Peru", "بيرو")], 1),
    ("What is the largest internal organ in the human body?", "ما أكبر عضو داخلي في جسم الإنسان؟", [("Liver", "الكبد"), ("Brain", "الدماغ"), ("Skin", "الجلد"), ("Intestine", "الأمعاء")], 1),
    ("What is the term for animals that eat only plants?", "ما اسم الحيوانات التي تأكل النباتات فقط؟", [("Herbivores", "عاشبة"), ("Carnivores", "لاحمة"), ("Omnivores", "كل شيء"), ("Scavengers", "آكلة جيف")], 1),
    ("What is the chemical symbol for iron?", "ما الرمز الكيميائي للحديد؟", [("Fe", "Fe"), ("Ir", "Ir"), ("In", "In"), ("I", "I")], 1),
    ("Which city is often called the Big Apple?", "أي مدينة تُسمى غالبًا التفاحة الكبيرة؟", [("New York City", "نيويورك"), ("Los Angeles", "لوس أنجلوس"), ("Chicago", "شيكاغو"), ("Boston", "بوسطن")], 1),
    ("What is the smallest country in the world by area?", "ما أصغر دولة في العالم مساحة؟", [("Vatican City", "الفاتيكان"), ("Monaco", "موناكو"), ("Malta", "مالطا"), ("San Marino", "سان مارينو")], 1),
    ("Which river is often considered the longest in the world?", "ما النهر الذي يُعتبر الأطول غالبًا؟", [("Nile", "النيل"), ("Amazon", "الأمازون"), ("Yangtze", "يانغتسي"), ("Mississippi", "المسيسيبي")], 1),
]


def generate_general(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(45)
    return [shuffle_preserve_pairs(qe, qa, opts, c, rng) for qe, qa, opts, c in _GENERAL_RAW]
