"""50 sports questions (EN + matching AR)."""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import shuffle_preserve_pairs

_SPORTS_RAW: list[tuple[str, str, list[tuple[str, str]], int]] = [
    ("How many players are on a football (soccer) team on the field?", "كم لاعبًا في فريق كرة القدم على الملعب؟", [("11", "11"), ("9", "9"), ("10", "10"), ("12", "12")], 1),
    ("Which country hosted the FIFA World Cup in 2022?", "أي دولة استضافت كأس العالم 2022؟", [("Qatar", "قطر"), ("Russia", "روسيا"), ("Brazil", "البرازيل"), ("Germany", "ألمانيا")], 1),
    ("How long is a marathon race (official distance)?", "ما طول سباق الماراثون الرسمي؟", [("42.195 km", "42.195 كم"), ("40 km", "40 كم"), ("50 km", "50 كم"), ("21 km", "21 كم")], 1),
    ("In tennis, what is a score of zero called?", "في التنس، ماذا يُسمى صفر النقاط؟", [("Love", "لَف"), ("Nil", "صفر"), ("Zero", "زيرو"), ("Blank", "فارغ")], 1),
    ("Which sport uses a shuttlecock?", "أي رياضة تستخدم الريشة (الشاتل كوك)؟", [("Badminton", "تنس الريشة"), ("Tennis", "التنس"), ("Squash", "الإسكواش"), ("Table tennis", "تنس الطاولة")], 1),
    ("How many minutes is a standard NBA quarter?", "كم دقيقة في ربع مباراة NBA؟", [("12", "12"), ("10", "10"), ("15", "15"), ("20", "20")], 1),
    ("Which trophy is awarded to the NFL champion?", "أي كأس يُمنح لبطل دوري كرة القدم الأمريكية؟", [("Super Bowl / Lombardi Trophy", "السوبر بول / كأس لومباردي"), ("Stanley Cup", "كأس ستانلي"), ("World Series", "السلسلة العالمية"), ("NBA Finals trophy", "كأس نهائي NBA")], 1),
    ("In which sport would you perform a slam dunk?", "في أي رياضة تُنفَّذ كرة السلة المعلّقة (سلام دانك)؟", [("Basketball", "كرة السلة"), ("Volleyball", "الكرة الطائرة"), ("Handball", "كرة اليد"), ("Netball", "نت بول")], 1),
    ("Which Grand Slam tournament is played on clay courts?", "أي بطولة غراند سلام تُلعب على ملاعب ترابية؟", [("French Open", "بطولة فرنسا المفتوحة"), ("Wimbledon", "ويمبلدون"), ("US Open", "الولايات المتحدة المفتوحة"), ("Australian Open", "أستراليا المفتوحة")], 1),
    ("What is the maximum score in a single ten-pin bowling game?", "ما أقصى نتيجة في لعبة بولينج عشرة أسياخ؟", [("300", "300"), ("200", "200"), ("250", "250"), ("500", "500")], 1),
    ("Which sport is associated with the Tour de France?", "أي رياضة ترتبط بجولة فرنسا؟", [("Cycling", "ركوب الدراجات"), ("Running", "الجري"), ("Swimming", "السباحة"), ("Skiing", "التزلج")], 1),
    ("How many holes in a standard round of golf?", "كم حفرة في جولة غولف قياسية؟", [("18", "18"), ("9", "9"), ("12", "12"), ("21", "21")], 1),
    ("In baseball, how many strikes for a batter out?", "في البيسبول، كم ضربة لإخراج الضارب؟", [("3", "3"), ("2", "2"), ("4", "4"), ("5", "5")], 1),
    ("Which sport features a scrum?", "أي رياضة يظهر فيها السكرم؟", [("Rugby", "الرغبي"), ("American football", "كرة القدم الأمريكية"), ("Water polo", "كرة الماء"), ("Hockey", "الهوكي")], 1),
    ("What color card means a player is sent off in football?", "ما لون البطاقة التي تعني طرد اللاعب في كرة القدم؟", [("Red", "حمراء"), ("Yellow", "صفراء"), ("Green", "خضراء"), ("Blue", "زرقاء")], 1),
    ("Which country is Lionel Messi from?", "من أي بلد ليونيل ميسي؟", [("Argentina", "الأرجنتين"), ("Spain", "إسبانيا"), ("Brazil", "البرازيل"), ("Portugal", "البرتغال")], 1),
    ("Which country is Cristiano Ronaldo from?", "من أي بلد كريستيانو رونالدو؟", [("Portugal", "البرتغال"), ("Spain", "إسبانيا"), ("Brazil", "البرازيل"), ("Italy", "إيطاليا")], 1),
    ("In volleyball, how many hits per side before the ball must go over?", "في الطائرة، كم ضربة لكل فريق قبل إرسال الكرة؟", [("3", "3"), ("2", "2"), ("4", "4"), ("Unlimited", "غير محدود")], 1),
    ("Which sport uses the terms birdie and eagle?", "أي رياضة تستخدم مصطلحي بيردي وإيغل؟", [("Golf", "الغولف"), ("Tennis", "التنس"), ("Cricket", "الكريكيت"), ("Baseball", "البيسبول")], 1),
    ("How many players start on a baseball team on the field?", "كم لاعبًا يبدأ في فريق البيسبول على الملعب؟", [("9", "9"), ("10", "10"), ("11", "11"), ("8", "8")], 1),
    ("Which sport is played at Wimbledon?", "أي رياضة تُلعب في ويمبلدون؟", [("Tennis", "التنس"), ("Cricket", "الكريكيت"), ("Rugby", "الرغبي"), ("Golf", "الغولف")], 1),
    ("What is the length of an Olympic swimming pool?", "ما طول حمام السباحة الأولمبي؟", [("50 meters", "50 مترًا"), ("25 meters", "25 مترًا"), ("100 meters", "100 مترًا"), ("33 meters", "33 مترًا")], 1),
    ("In Formula 1, what does a checkered flag mean?", "في الفورمولا 1، ماذا تعني العلم المربّع؟", [("Race finished", "انتهى السباق"), ("Danger", "خطر"), ("Slow down", "بطء"), ("Pit stop", "وقفة الصيانة")], 1),
    ("Which sport uses a puck?", "أي رياضة تستخدم قرص الهوكي (باك)؟", [("Ice hockey", "الهوكي على الجليد"), ("Field hockey", "الهوكي الميداني"), ("Lacrosse", "لاكروس"), ("Polo", "البولو")], 1),
    ("What is a hat-trick in football?", "ما الهاتريك في كرة القدم؟", [("Three goals by one player in a match", "ثلاثة أهداف من لاعب واحد في مباراة"), ("Three yellow cards", "ثلاث بطاقات صفراء"), ("Three saves", "ثلاث تصديات"), ("Three assists", "ثلاث تمريرات حاسمة")], 1),
    ("Which sport is known as America's pastime?", "ما الرياضة المعروفة بترفيه أمريكا؟", [("Baseball", "البيسبول"), ("Basketball", "كرة السلة"), ("American football", "كرة القدم الأمريكية"), ("Ice hockey", "الهوكي")], 1),
    ("How many players per team in beach volleyball?", "كم لاعبًا لكل فريق في الكرة الطائرة الشاطئية؟", [("2", "2"), ("3", "3"), ("4", "4"), ("6", "6")], 1),
    ("Which sport is associated with Augusta National?", "أي رياضة ترتبط بأوغستا ناشونال؟", [("Golf", "الغولف"), ("Tennis", "التنس"), ("Cricket", "الكريكيت"), ("Baseball", "البيسبول")], 1),
    ("What is the diameter of a basketball hoop in inches?", "ما قطر حلقة كرة السلة بالبوصة؟", [("18", "18"), ("16", "16"), ("17", "17"), ("20", "20")], 1),
    ("Which country won the FIFA World Cup in 2018?", "أي فريق فاز بكأس العالم 2018؟", [("France", "فرنسا"), ("Germany", "ألمانيا"), ("Brazil", "البرازيل"), ("Argentina", "الأرجنتين")], 1),
    ("In cricket, how many runs for a six?", "في الكريكيت، كم ركضة للضربة السداسية؟", [("6", "6"), ("4", "4"), ("5", "5"), ("10", "10")], 1),
    ("Which sport uses a mallet and horses?", "أي رياضة تستخدم المطرقة والخيول؟", [("Polo", "البولو"), ("Croquet", "الكروكيه"), ("Horse racing", "سباق الخيل"), ("Dressage", "الفروسية")], 1),
    ("What is the maximum break in snooker?", "ما أقصى بريك في السنوكر؟", [("147", "147"), ("140", "140"), ("150", "150"), ("155", "155")], 1),
    ("Which sport is played on a sheet with stones and brooms?", "أي رياضة تُلعب على ممر مع أحجار ومكانس؟", [("Curling", "الكرلنغ"), ("Ice hockey", "الهوكي"), ("Bobsled", "الزلاجات"), ("Figure skating", "التزلج الفني")], 1),
    ("How many periods in a standard ice hockey game?", "كم فترة في مباراة الهوكي القياسية؟", [("3", "3"), ("2", "2"), ("4", "4"), ("5", "5")], 1),
    ("Which sport uses a foil, épée, or sabre?", "أي رياضة تستخدم الشفرة أو الإيبيه أو السيف؟", [("Fencing", "المبارزة"), ("Archery", "الرماية"), ("Judo", "الجودو"), ("Boxing", "الملاكمة")], 1),
    ("What is the national sport of Canada (often cited)?", "ما الرياضة الوطنية في كندا (غالبًا)؟", [("Ice hockey", "الهوكي على الجليد"), ("Lacrosse", "لاكروس"), ("Soccer", "كرة القدم"), ("Basketball", "كرة السلة")], 1),
    ("In boxing, what does KO mean?", "في الملاكمة، ماذا تعني KO؟", [("Knockout", "ضربة قاضية"), ("Keep out", "ابق خارجًا"), ("King of ring", "ملك الحلبة"), ("Kick off", "انطلاق")], 1),
    ("Which sport measures performance in decathlon?", "أي رياضة تقيس الأداء في العشاري؟", [("Athletics / track and field", "ألعاب القوى"), ("Swimming", "السباحة"), ("Weightlifting", "رفع الأثقال"), ("Cycling", "الدراجات")], 1),
    ("What is offside in football?", "ما التسلل في كرة القدم؟", [("Attacking player ahead of ball and second-last defender", "مهاجم متقدم على الكرة وقبل المدافع قبل الأخير"), ("Goalkeeper error", "خطأ الحارس"), ("Handball", "لمس الكرة باليد"), ("Foul in box", "خطأ في المنطقة")], 1),
    ("Which sport is played in the NBA?", "أي رياضة تُلعب في NBA؟", [("Basketball", "كرة السلة"), ("Baseball", "البيسبول"), ("American football", "كرة القدم الأمريكية"), ("Ice hockey", "الهوكي")], 1),
    ("How many points is a touchdown worth in American football (before extra point)?", "كم نقطة لللمسة الأرضية قبل النقطة الإضافية؟", [("6", "6"), ("7", "7"), ("5", "5"), ("3", "3")], 1),
    ("Which sport uses wickets and a crease?", "أي رياضة تستخدم الويكت والخط؟", [("Cricket", "الكريكيت"), ("Baseball", "البيسبول"), ("Softball", "السوفت بول"), ("Rounders", "الراوندرز")], 1),
    ("What is a medley relay in swimming?", "ما سباق التناوب المتنوع في السباحة؟", [("Team swims different strokes in order", "الفريق يسبح أنماطًا مختلفة بالترتيب"), ("Only freestyle", "حر فقط"), ("Only backstroke", "ظهر فقط"), ("Solo race", "سباق فردي")], 1),
    ("Which sport is associated with the Ryder Cup?", "أي رياضة ترتبط بكأس رايدر؟", [("Golf", "الغولف"), ("Tennis", "التنس"), ("Rugby", "الرغبي"), ("Cricket", "الكريكيت")], 1),
    ("What does MMA stand for?", "ماذا تعني MMA؟", [("Mixed Martial Arts", "فنون قتالية مشتركة"), ("Major Match Association", "جمعية المباريات الكبرى"), ("Multi Muscle Activity", "نشاط عضلي متعدد"), ("Motor Marathon Arena", "ساحة ماراثون المحركات")], 1),
    ("Which sport is played at the Super Bowl?", "أي رياضة تُلعب في السوبر بول؟", [("American football", "كرة القدم الأمريكية"), ("Soccer", "كرة القدم"), ("Basketball", "كرة السلة"), ("Baseball", "البيسبول")], 1),
    ("How many substitutions are allowed in standard football (FIFA laws overview)?", "كم تبديلًا مسموحًا في كرة القدم (نظرة عامة)؟", [("Usually up to 5 in many competitions", "عادة حتى 5 في كثير من البطولات"), ("Unlimited", "غير محدود"), ("2", "2"), ("11", "11")], 1),
    ("What is a yellow card in football?", "ما البطاقة الصفراء في كرة القدم؟", [("Warning for a foul", "تحذير بسبب خطأ"), ("Player sent off", "طرد"), ("Goal scored", "هدف"), ("Substitution", "تبديل")], 1),
    ("Which sport is known for the Stanley Cup?", "أي رياضة معروفة بكأس ستانلي؟", [("Ice hockey", "الهوكي على الجليد"), ("Basketball", "كرة السلة"), ("Baseball", "البيسبول"), ("Soccer", "كرة القدم")], 1),
]


def generate_sports(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(44)
    return [shuffle_preserve_pairs(qe, qa, opts, c, rng) for qe, qa, opts, c in _SPORTS_RAW]
