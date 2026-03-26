"""50 cars & automotive questions (EN + matching AR)."""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import shuffle_preserve_pairs

# Each: (q_en, q_ar, [(o1e,o1a)...x4], correct_1based)
_CAR_RAW: list[tuple[str, str, list[tuple[str, str]], int]] = [
    ("Which company produces the Mustang?", "أي شركة تصنع سيارة فورد موستانغ؟", [("Ford", "فورد"), ("Toyota", "تويوتا"), ("Honda", "هوندا"), ("Hyundai", "هيونداي")], 1),
    ("Which country is Toyota headquartered in?", "في أي بلد يقع المقر الرئيسي لتويوتا؟", [("Japan", "اليابان"), ("South Korea", "كوريا الجنوبية"), ("China", "الصين"), ("Germany", "ألمانيا")], 1),
    ("What does BMW stand for (original meaning)?", "ماذا تعني حروف BMW في الأصل؟", [("Bayerische Motoren Werke", "الورش البافارية للمحركات"), ("British Motor Works", "أعمال المحركات البريطانية"), ("Berlin Motor Werke", "ورش برلين للمحركات"), ("Belgian Motor Works", "أعمال المحركات البلجيكية")], 1),
    ("Which brand uses the slogan 'The Ultimate Driving Machine'?", "أي علامة تستخدم شعار \"أفضل آلة للقيادة\"؟", [("BMW", "بي إم دبليو"), ("Mercedes-Benz", "مرسيدس بنز"), ("Audi", "أودي"), ("Lexus", "لكزس")], 1),
    ("What is the best-selling electric car brand worldwide (typical recent years)?", "ما العلامة الأكثر مبيعًا للسيارات الكهربائية عالميًا في السنوات الأخيرة؟", [("Tesla", "تسلا"), ("Nissan", "نيسان"), ("BYD", "بي واي دي"), ("Volkswagen", "فولكس فاجن")], 1),
    ("Which brand produces the 911 sports car?", "أي علامة تصنع سيارة 911 الرياضية؟", [("Porsche", "بورشه"), ("Ferrari", "فيراري"), ("Lamborghini", "لامبورغيني"), ("Audi", "أودي")], 1),
    ("Which company owns the Land Rover brand?", "أي شركة تمتلك علامة لاند روفر؟", [("Jaguar Land Rover (Tata)", "جاغوار لاند روفر (تاتا)"), ("Ford", "فورد"), ("GM", "جنرال موتورز"), ("Volkswagen", "فولكس فاجن")], 1),
    ("What fuel do most diesel engines use?", "ما الوقود الذي تستخدمه معظم محركات الديزل؟", [("Diesel fuel", "وقود الديزل"), ("Petrol / gasoline", "البنزين"), ("Electricity only", "كهرباء فقط"), ("LPG only", "غاز البترول المسال فقط")], 1),
    ("What does ABS stand for in cars?", "ماذا تعني ABS في السيارات؟", [("Anti-lock Braking System", "نظام منع انغلاق المكابح"), ("Automatic Brake Support", "دعم الفرامل التلقائي"), ("Advanced Battery System", "نظام بطارية متقدم"), ("Air Bag Safety", "سلامة الوسائد الهوائية")], 1),
    ("Which part connects the engine to the wheels?", "أي جزء يربط المحرك بالعجلات؟", [("Transmission / gearbox", "ناقل الحركة / علبة السرعة"), ("Radiator", "المبرد"), ("Battery", "البطارية"), ("Alternator", "المولد")], 1),
    ("What is a hybrid car?", "ما المقصود بالسيارة الهجينة؟", [("Uses petrol engine + electric motor", "تستخدم محرك بنزين + محرك كهربائي"), ("Runs only on petrol", "تعمل بالبنزين فقط"), ("Runs only on diesel", "تعمل بالديزل فقط"), ("Has no engine", "بلا محرك")], 1),
    ("Which company makes the Corolla model?", "أي شركة تصنع طراز كورولا؟", [("Toyota", "تويوتا"), ("Honda", "هوندا"), ("Nissan", "نيسان"), ("Mazda", "مازدا")], 1),
    ("Which company makes the Civic model?", "أي شركة تصنع طراز سيفيك؟", [("Honda", "هوندا"), ("Toyota", "تويوتا"), ("Hyundai", "هيونداي"), ("Kia", "كيا")], 1),
    ("What does SUV stand for?", "ماذا تعني SUV؟", [("Sport Utility Vehicle", "سيارة رياضية متعددة الاستخدامات"), ("Super Urban Vehicle", "سيارة حضرية فائقة"), ("Small Utility Van", "شاحنة صغيرة متعددة الاستخدام"), ("Speed Utility Vehicle", "سيارة سرعة متعددة الاستخدامات")], 1),
    ("Which safety device inflates in a crash?", "أي جهاز أمان ينتفخ عند الاصطدام؟", [("Airbag", "الوسادة الهوائية"), ("Seat belt only", "حزام الأمان فقط"), ("ABS", "نظام ABS"), ("ESP", "نظام ESP")], 1),
    ("What is the main purpose of engine oil?", "ما الغرض الرئيسي من زيت المحرك؟", [("Lubrication and cooling", "التزييت والتبريد"), ("Only cleaning the paint", "تنظيف الطلاء فقط"), ("Charging the battery", "شحن البطارية"), ("Cooling the cabin only", "تبريد المقصورة فقط")], 1),
    ("Which German brand has a four-ring logo?", "أي علامة ألمانية شعارها أربع حلقات؟", [("Audi", "أودي"), ("BMW", "بي إم دبليو"), ("Mercedes-Benz", "مرسيدس بنز"), ("Opel", "أوبل")], 1),
    ("Which brand uses a prancing horse logo?", "أي علامة تستخدم شعار حصان متوهج؟", [("Ferrari", "فيراري"), ("Ford", "فورد"), ("Porsche", "بورشه"), ("Lamborghini", "لامبورغيني")], 1),
    ("What is a turbocharger?", "ما المقصود بالشاحن التوربيني؟", [("Uses exhaust gas to compress air into the engine", "يستخدم غاز العادم لضغط الهواء داخل المحرك"), ("Electric battery charger", "شاحن بطارية كهربائي"), ("Automatic gearbox", "علبة سرعة أوتوماتيكية"), ("Brake booster", "معزز الفرامل")], 1),
    ("Which type of drive sends power to all four wheels?", "أي نوع دفع يوجّه القوة إلى العجلات الأربع؟", [("AWD / 4WD", "دفع رباعي / للعجلات الأربع"), ("FWD only", "دفع أمامي فقط"), ("RWD only", "دفع خلفي فقط"), ("Two-wheel trailer", "مقطورة بعجلتين")], 1),
    ("What does EV stand for?", "ماذا تعني EV؟", [("Electric Vehicle", "مركبة كهربائية"), ("Extra Velocity", "سرعة إضافية"), ("Engine Valve", "صمام المحرك"), ("European Version", "نسخة أوروبية")], 1),
    ("Which brand is famous for the blue oval logo?", "أي علامة مشهورة بالشعار البيضاوي الأزرق؟", [("Ford", "فورد"), ("Toyota", "تويوتا"), ("Honda", "هوندا"), ("Nissan", "نيسان")], 1),
    ("What is horsepower (HP) a measure of?", "ما الذي تقيسه وحدة الحصان (HP)؟", [("Engine power output", "قدرة المخرجات للمحرك"), ("Fuel tank size", "حجم خزان الوقود"), ("Top speed in km/h", "السرعة القصوى بالكم/س"), ("Number of seats", "عدد المقاعد")], 1),
    ("Which part reduces friction between moving engine parts?", "أي جزء يقلل الاحتكاك بين أجزاء المحرك المتحركة؟", [("Bearings and oil film", "المحامل وطبقة الزيت"), ("Windshield", "الزجاج الأمامي"), ("Tires only", "الإطارات فقط"), ("Radiator fan", "مروحة المبرد")], 1),
    ("What is a catalytic converter?", "ما المقصود بمحول الحفاز؟", [("Reduces harmful exhaust emissions", "يقلل انبعاثات العادم الضارة"), ("Increases engine noise", "يزيد ضوضاء المحرك"), ("Charges the battery", "يشحن البطارية"), ("Cools the cabin", "يبرد المقصورة")], 1),
    ("Which luxury brand is a division of Toyota?", "أي علامة فاخرة هي قسم من تويوتا؟", [("Lexus", "لكزس"), ("Acura", "أكيورا"), ("Infiniti", "إنفينيتي"), ("Genesis", "جينيسيس")], 1),
    ("Which luxury brand is a division of Honda?", "أي علامة فاخرة هي قسم من هوندا؟", [("Acura", "أكيورا"), ("Lexus", "لكزس"), ("Infiniti", "إنفينيتي"), ("Cadillac", "كاديلاك")], 1),
    ("What is torque in simple terms?", "ما عزم الدوران ببساطة؟", [("Rotational force from the engine", "قوة دوران من المحرك"), ("Maximum speed", "السرعة القصوى"), ("Fuel consumption", "استهلاك الوقود"), ("Battery voltage", "جهد البطارية")], 1),
    ("Which system helps keep the car stable when turning?", "أي نظام يساعد على ثبات السيارة عند المنعطفات؟", [("ESC / ESP (electronic stability)", "نظام الثبات الإلكتروني"), ("Only the horn", "البوري فقط"), ("Radio", "الراديو"), ("Air conditioning", "التكييف")], 1),
    ("What is a CVT transmission?", "ما ناقل الحركة CVT؟", [("Continuously variable transmission", "ناقل حركة متغير باستمرار"), ("Manual only", "يدوي فقط"), ("Dual-clutch only", "قابض مزدوج فقط"), ("Only for trucks", "للشاحنات فقط")], 1),
    ("Which company is known for the Silverado pickup?", "أي شركة مشهورة ببيك أب سيلفرادو؟", [("Chevrolet (GM)", "شيفروليه (جنرال موتورز)"), ("Ford", "فورد"), ("Ram", "رام"), ("Toyota", "تويوتا")], 1),
    ("Which company makes the F-150 pickup (very popular in the US)?", "أي شركة تصنع بيك أب F-150؟", [("Ford", "فورد"), ("Chevrolet", "شيفروليه"), ("GMC", "جي إم سي"), ("Toyota", "تويوتا")], 1),
    ("What is regenerative braking in EVs?", "ما الكبح التجديدي في السيارات الكهربائية؟", [("Recovers energy to the battery when slowing", "يستعيد طاقة للبطارية عند التباطؤ"), ("Uses only the handbrake", "يستخدم فرملة اليد فقط"), ("Disables ABS", "يعطل ABS"), ("Increases fuel use", "يزيد استهلاك الوقود")], 1),
    ("Which Italian city is famous for Ferrari’s headquarters?", "أي مدينة إيطالية يقع فيها مقر فيراري؟", [("Maranello", "مارانيلو"), ("Milan", "ميلانو"), ("Rome", "روما"), ("Turin", "تورينو")], 1),
    ("What is octane rating related to?", "ما علاقة رقم الأوكتان؟", [("Fuel knock resistance / quality", "مقاومة الاحتراق الذاتي / جودة الوقود"), ("Tire pressure", "ضغط الإطارات"), ("Oil viscosity", "لزوجة الزيت"), ("Battery capacity", "سعة البطارية")], 1),
    ("Which brand produces the Model 3 and Model Y?", "أي علامة تصنع موديل 3 وموديل Y؟", [("Tesla", "تسلا"), ("BMW", "بي إم دبليو"), ("Nissan", "نيسان"), ("Hyundai", "هيونداي")], 1),
    ("What is a differential in a car?", "ما المقصود بالديفرنشيل في السيارة؟", [("Splits torque between wheels on an axle", "يوزع عزم الدوران بين عجلات المحور"), ("Steering wheel", "عجلة القيادة"), ("Brake pedal", "دواسة الفرامل"), ("Fuel pump", "مضخة الوقود")], 1),
    ("Which country is Volkswagen headquartered in?", "في أي بلد يقع مقر فولكس فاجن؟", [("Germany", "ألمانيا"), ("France", "فرنسا"), ("Italy", "إيطاليا"), ("USA", "الولايات المتحدة")], 1),
    ("Which country is Renault headquartered in?", "في أي بلد يقع مقر رينو؟", [("France", "فرنسا"), ("Germany", "ألمانيا"), ("Spain", "إسبانيا"), ("Japan", "اليابان")], 1),
    ("What is ADAS?", "ما المقصود بـ ADAS؟", [("Advanced Driver Assistance Systems", "أنظمة مساعدة السائق المتقدمة"), ("Automatic Door And Seat", "باب ومقعد أوتوماتيكي"), ("Airbag Deployment And Safety", "انتشار الوسائد والسلامة"), ("Anti-Diesel Additive System", "نظام إضافات مضاد للديزل")], 1),
    ("Which sensor is often used for adaptive cruise control?", "أي مستشعر يُستخدم غالبًا في تثبيت السرعة التكيفي؟", [("Radar / camera", "رادار / كاميرا"), ("Oil dipstick", "ميزان زيت"), ("Spark plug", "شمعة الإشعال"), ("Windshield wiper", "مساحة الزجاج")], 1),
    ("What is wheel alignment for?", "ما الغرض من ضبط زوايا العجلات؟", [("Correct tire angles for even wear and handling", "تصحيح زوايا الإطارات للتآكل والتعامل"), ("Painting wheels", "طلاء العجلات"), ("Changing tire size", "تغيير مقاس الإطار"), ("Washing brakes", "غسل الفرامل")], 1),
    ("Which fluid is usually red or pink in automatic transmissions?", "أي سائل يكون غالبًا أحمر أو وردي في ناقل الحركة الأوتوماتيكي؟", [("ATF (automatic transmission fluid)", "زيت ناقل الحركة الأوتوماتيكي"), ("Engine coolant only", "مبرد المحرك فقط"), ("Brake fluid only", "سائل الفرامل فقط"), ("Windshield washer", "ماء مساحات الزجاج")], 1),
    ("What is a spark plug used for?", "ما استخدام شمعة الإشعال؟", [("Ignites fuel–air mixture in petrol engines", "تشعل خليط الوقود والهواء في محركات البنزين"), ("Cools the radiator", "تبرد المبرد"), ("Pumps fuel", "تضخ الوقود"), ("Steers the wheels", "توجّه العجلات")], 1),
    ("Which company owns Volvo Cars (passenger cars division)?", "أي شركة تمتلك فولفو للسيارات؟", [("Geely (China)", "جيلي (الصين)"), ("Ford", "فورد"), ("Toyota", "تويوتا"), ("VW Group", "مجموعة فولكس فاجن")], 1),
    ("What is lane-keeping assist?", "ما مساعد الحفاظ على المسار؟", [("Helps steer to stay in lane", "يساعد على التوجيه للبقاء في المسار"), ("Keeps windows closed", "يغلق النوافذ"), ("Locks doors automatically", "يقفل الأبواب"), ("Adjusts radio volume", "يضبط صوت الراديو")], 1),
    ("What is oversteer?", "ما الانزلاق الزائد (أوفرستير)؟", [("Rear loses grip, tail swings out", "الخلف يفقد تماسكًا ويخرج المؤخرة"), ("Front pushes wide only", "الأمام ينحرف فقط"), ("Car goes straight only", "السيارة تمشي مستقيمة فقط"), ("Brakes lock", "تغلق الفرامل")], 1),
    ("What is understeer?", "ما الانزلاق الناقص (أندرستير)؟", [("Front loses grip, car pushes wide", "الأمام يفقد تماسكًا وتنحرف السيارة للخارج"), ("Rear swings out", "المؤخرة تنحرف"), ("Engine stalls", "المحرك يطفأ"), ("Battery dies", "البطارية تموت")], 1),
    ("Which document proves legal vehicle ownership in many countries?", "أي وثيقة تثبت ملكية المركبة قانونيًا في كثير من البلدان؟", [("Title / registration", "سند الملكية / التسجيل"), ("Only the radio manual", "دليل الراديو فقط"), ("Tire warranty", "ضمان الإطارات"), ("Car wash receipt", "إيصال غسيل")], 1),
    ("What is VIN?", "ما هو رقم الهيكل VIN؟", [("Vehicle Identification Number (unique code)", "رقم تعريف المركبة (رمز فريد)"), ("Vehicle Insurance Number", "رقم التأمين"), ("Voltage In Neutral", "جهد في الحياد"), ("Very Important Notice", "إشعار مهم جدًا")], 1),
]


def generate_cars(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(43)
    out: list[dict] = []
    for q_en, q_ar, opts, correct in _CAR_RAW:
        out.append(shuffle_preserve_pairs(q_en, q_ar, opts, correct, rng))
    assert len(out) == 50
    return out
