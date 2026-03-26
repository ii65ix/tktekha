"""50 movies & cinema questions (EN + matching AR)."""

from __future__ import annotations

import random

from quiz.data.bilingual_helpers import shuffle_preserve_pairs

_MOVIES_RAW: list[tuple[str, str, list[tuple[str, str]], int]] = [
    ("Which award show famously gives 'Oscars'?", "أي حفل يمنح جوائز الأوسكار الشهيرة؟", [("The Academy Awards", "جوائز الأكاديمية"), ("The Grammys", "الغرامي"), ("The Tonys", "الطوني"), ("The ESPYs", "إسبي")], 1),
    ("Who directed the 1997 film Titanic?", "من أخرج فيلم تيتانيك 1997؟", [("James Cameron", "جيمس كاميرون"), ("Steven Spielberg", "ستيفن سبيلبرغ"), ("Christopher Nolan", "كريستوفر نولان"), ("Ridley Scott", "ريدلي سكوت")], 1),
    ("Who created the Star Wars franchise?", "من أنشأ سلسلة ستار وورز؟", [("George Lucas", "جورج لوكاس"), ("Stan Lee", "ستان لي"), ("J.K. Rowling", "ج. ك. رولينغ"), ("Peter Jackson", "بيتر جاكسون")], 1),
    ("What is the first Harry Potter film called?", "كيف يُسمى أول فيلم هاري بوتر؟", [("Harry Potter and the Philosopher's Stone (Sorcerer's Stone in the US)", "هاري بوتر وحجر الفيلسوف (حجر الساحر في الولايات المتحدة)"), ("Harry Potter and the Goblet of Fire", "هاري بوتر وكأس النار"), ("Harry Potter and the Deathly Hallows", "هاري بوتر ومقدّسات الموت"), ("Harry Potter and the Prisoner of Azkaban", "هاري بوتر وسجين أزكابان")], 1),
    ("The Marvel Cinematic Universe (MCU) is mainly based on characters from where?", "عالم مارفل السينمائي مستند أساسًا إلى شخصيات من أين؟", [("Marvel Comics", "قصص مارفل المصورة"), ("DC Comics", "قصص دي سي المصورة"), ("Manga only", "مانغا فقط"), ("Fairy tales only", "حكايات خرافية فقط")], 1),
    ("James Bond is most associated with which country's spy films?", "جيمس بوند مرتبط بأفلام تجسس أي بلد؟", [("United Kingdom", "المملكة المتحدة"), ("Russia", "روسيا"), ("France", "فرنسا"), ("Japan", "اليابان")], 1),
    ("Which Disney animated film features Simba?", "أي فيلم رسوم متحركة من ديزني يظهر فيه سيمبا؟", [("The Lion King", "الملك الأسد"), ("Frozen", "فروزن"), ("Moana", "موانا"), ("Aladdin", "علاء الدين")], 1),
    ("Which song became a huge hit from Disney's Frozen?", "أي أغنية حققت نجاحًا كبيرًا من فيلم فروزن؟", [("Let It Go", "لِت إت غو"), ("Circle of Life", "دائرة الحياة"), ("A Whole New World", "عالم جديد تمامًا"), ("Under the Sea", "تحت البحر")], 1),
    ("Who directed The Shawshank Redemption?", "من أخرج فيلم الخلاص من شاوشانك؟", [("Frank Darabont", "فرانك دارابونت"), ("Martin Scorsese", "مارتن سكورسيزي"), ("Quentin Tarantino", "كوينتن تارانتينو"), ("Clint Eastwood", "كلينت إيستوود")], 1),
    ("Who directed The Godfather (1972)?", "من أخرج العراب 1972؟", [("Francis Ford Coppola", "فرانسيس فورد كوبولا"), ("Steven Spielberg", "ستيفن سبيلبرغ"), ("Alfred Hitchcock", "ألفريد هيتشكوك"), ("Woody Allen", "وودي ألن")], 1),
    ("Who directed Pulp Fiction?", "من أخرج فيلم خرافات العنف؟", [("Quentin Tarantino", "كوينتن تارانتينو"), ("Guy Ritchie", "غاي ريتشي"), ("David Fincher", "ديفيد فينشر"), ("Coen Brothers", "الأخوان كوين")], 1),
    ("Who directed Inception?", "من أخرج فيلم الاستهلال؟", [("Christopher Nolan", "كريستوفر نولان"), ("James Cameron", "جيمس كاميرون"), ("Ridley Scott", "ريدلي سكوت"), ("Denis Villeneuve", "دين فيلنوف")], 1),
    ("The Matrix was directed by whom (credited)?", "من أخرج المصفوفة (الاعتمادات)؟", [("The Wachowskis", "الواشوفسكي"), ("Christopher Nolan", "كريستوفر نولان"), ("Peter Jackson", "بيتر جاكسون"), ("James Wan", "جيمس وان")], 1),
    ("Spider-Man is most associated with which comics publisher?", "سبايدرمان مرتبط بأي دار قصص مصورة؟", [("Marvel", "مارفل"), ("DC", "دي سي"), ("Dark Horse", "دارك هورس"), ("Image", "إيمج")], 1),
    ("Batman is most associated with which comics publisher?", "باتمان مرتبط بأي دار قصص مصورة؟", [("DC", "دي سي"), ("Marvel", "مارفل"), ("IDW", "آي دي دبليو"), ("Valiant", "فاليانت")], 1),
    ("What is Superman's home planet?", "ما كوكب سوبرمان الأصلي؟", [("Krypton", "كربتون"), ("Earth", "الأرض"), ("Mars", "المريخ"), ("Vulcan", "فولكان")], 1),
    ("What is the nickname of the Academy Award statuette?", "ما اللقب الشائع لتمثال جائزة الأكاديمية؟", [("Oscar", "أوسكار"), ("Tony", "طوني"), ("Emmy", "إيمي"), ("Grammy", "غرامي")], 1),
    ("The Cannes Film Festival is held annually in which country?", "مهرجان كان السينمائي يُقام سنويًا في أي بلد؟", [("France", "فرنسا"), ("Italy", "إيطاليا"), ("Spain", "إسبانيا"), ("Germany", "ألمانيا")], 1),
    ("Which city is famously tied to 'Hollywood'?", "أي مدينة ترتبط بشهرة هوليوود؟", [("Los Angeles area, California", "منطقة لوس أنجلوس، كاليفورنيا"), ("New York City", "نيويورك"), ("London", "لندن"), ("Paris", "باريس")], 1),
    ("What does CGI stand for in film?", "ماذا تعني CGI في السينما؟", [("Computer-generated imagery", "صور مولّدة بالحاسوب"), ("Cinematic General Index", "مؤشر سينمائي عام"), ("Classic German Import", "استيراد ألماني كلاسيكي"), ("Central Graphics Interface", "واجهة رسوم مركزية")], 1),
    ("What is a movie sequel?", "ما تتمة الفيلم؟", [("A follow-up story continuing the franchise", "قصة لاحقة تتابع السلسلة"), ("A silent film", "فيلم صامت"), ("A trailer only", "إعلان دعائي فقط"), ("A deleted scene", "مشهد محذوف")], 1),
    ("What is a prequel?", "ما الفيلم السابق زمنيًا؟", [("A story set before the original", "قصة تقع قبل الأصل"), ("A story set after the ending", "قصة بعد النهاية"), ("A remake always", "إعادة إنتاج دائمًا"), ("A documentary only", "وثائقي فقط")], 1),
    ("A film adapted from a novel is called what?", "الفيلم المأخوذ من رواية يُسمى ماذا؟", [("An adaptation", "اقتباس"), ("A sequel", "تتمة"), ("A spin-off only", "اشتقاق فقط"), ("A biopic always", "سيرة ذاتية دائمًا")], 1),
    ("The Lord of the Rings films are mainly what genre?", "أفلام سيد الخواتم غالبًا أي نوع؟", [("Epic fantasy", "فنتازيا ملحمية"), ("Romantic comedy", "كوميديا رومانسية"), ("Horror", "رعب"), ("Western", "غرب أمريكي")], 1),
    ("What is a horror film designed to do?", "ما الغرض من فيلم الرعب؟", [("Scare or unsettle the audience", "إخافة الجمهور أو إزعاجه"), ("Always teach cooking", "تعليم الطبخ دائمًا"), ("Show sports only", "رياضة فقط"), ("Replace news", "استبدال الأخبار")], 1),
    ("Which studio is famous for Toy Story and many animated features?", "أي استوديو مشهور بفيلم حكاية لعبة والكثير من الرسوم؟", [("Pixar", "بيكسار"), ("BBC", "بي بي سي"), ("NBC", "إن بي سي"), ("CNN", "سي إن إن")], 1),
    ("What was Pixar's first feature-length film?", "ما أول فيلم طويل لبيكسار؟", [("Toy Story", "حكاية لعبة"), ("Finding Nemo", "البحث عن نيمو"), ("Monsters, Inc.", "شركة المرعبين المحدودة"), ("Cars", "سيارات")], 1),
    ("Finding Nemo mainly features what animal?", "البحث عن نيمو يظهر أساسًا أي حيوان؟", [("A clownfish", "سمكة المهرج"), ("A shark only", "قرش فقط"), ("A whale only", "حوت فقط"), ("A seagull", "نورس")], 1),
    ("Which Oscar category honors the overall best film of the year?", "أي فئة أوسكار تكرّم أفضل فيلم عامًا؟", [("Best Picture", "أفضل فيلم"), ("Best Sound Mixing", "أفضل مزج صوت"), ("Best Costume Design", "أفضل تصميم أزياء"), ("Best Visual Effects", "أفضل مؤثرات بصرية")], 1),
    ("Which category honors acting performance (female) in a supporting role?", "أي فئة تكرّم أداء ممثلة بدور ثانوي؟", [("Best Supporting Actress", "أفضل ممثلة مساعدة"), ("Best Actress", "أفضل ممثلة"), ("Best Director", "أفضل مخرج"), ("Best Original Song", "أفضل أغنية أصلية")], 1),
    ("What is 'box office' commonly referring to?", "ما المقصود شائعًا بـ شباك التذاكر؟", [("Ticket sales revenue", "إيرادات تذاكر"), ("A physical box only", "صندوق فقط"), ("DVD sales only", "مبيعات دي في دي فقط"), ("Critics' scores only", "درجات النقاد فقط")], 1),
    ("What is a movie trailer?", "ما إعلان الفيلم التشويقي؟", [("A short preview advertisement", "معاينة دعائية قصيرة"), ("The full film", "الفيلم كاملًا"), ("End credits only", "شارة نهاية فقط"), ("A script book", "كتاب سيناريو")], 1),
    ("What are opening or closing credits?", "ما شارة البداية أو النهاية؟", [("Lists of cast and crew", "قائمة الممثلين والطاقم"), ("Only the ticket price", "سعر التذكرة فقط"), ("Deleted scenes", "مشاهد محذوفة"), ("Subtitles language", "لغة الترجمة")], 1),
    ("What is a post-credits scene?", "ما مشهد ما بعد الشارة؟", [("A short extra scene after the credits", "مشهد إضافي قصير بعد الشارة"), ("The first scene of the film", "أول مشهد في الفيلم"), ("A trailer for another studio", "إعلان لاستوديو آخر"), ("The director's home video", "فيديو منزل للمخرج")], 1),
    ("What does MCU stand for?", "ماذا تعني MCU؟", [("Marvel Cinematic Universe", "العالم السينمائي لمارفل"), ("Movie Critics Union", "اتحاد نقاد الأفلام"), ("Main Camera Unit", "وحدة الكاميرا الرئيسية"), ("Music Copyright Unit", "وحدة حقوق الموسيقى")], 1),
    ("Which universe includes Batman and Wonder Woman on screen (common branding)?", "أي عالم يضم باتمان ووندر وومن على الشاشة (تسمية شائعة)؟", [("DC films / DC Extended Universe (branding varies)", "أفلام دي سي / العالم الممتد (تختلف التسمية)"), ("MCU", "عالم مارفل"), ("Star Trek", "ستار تريك"), ("Fast & Furious only", "فاست أند فيوريوس فقط")], 1),
    ("What is film noir often associated with?", "ما الذي يرتبط به الفيلم نوار غالبًا؟", [("Dark crime dramas and moody lighting", "دراما جريمة مظلمة وإضاءة صامتة"), ("Only cartoons", "رسوم متحركة فقط"), ("Musicals only", "موسيقية فقط"), ("Cooking shows", "برامج طبخ")], 1),
    ("A Western genre film is typically set where?", "فيلم الغرب الأمريكي يقع أحداثه عادةً أين؟", [("American frontier / Old West settings", "الحدود الأمريكية / الغرب القديم"), ("Only underwater", "تحت الماء فقط"), ("Only Mars", "المريخ فقط"), ("Only Antarctica", "القطب الجنوبي فقط")], 1),
    ("What is a musical film?", "ما الفيلم الموسيقي؟", [("A film where songs advance the story", "فيلم تدفع فيه الأغاني القصة"), ("A silent film", "فيلم صامت"), ("A sports documentary", "وثائقي رياضي"), ("A horror without music", "رعب بلا موسيقى")], 1),
    ("What is a documentary?", "ما الوثائقي؟", [("Non-fiction film about real topics", "فيلم غير خيالي عن مواضيع حقيقية"), ("Always animated fiction", "خيال متحرك دائمًا"), ("Only superhero fights", "قتال أبطال فقط"), ("Only comedy sketches", "مشاهد كوميدية فقط")], 1),
    ("What are subtitles?", "ما الترجمة النصية؟", [("Text on screen translating dialogue", "نص على الشاشة يترجم الحوار"), ("Loud sound effects", "مؤثرات صاخبة"), ("3D glasses", "نظارات ثلاثية الأبعاد"), ("Ticket barcode", "باركود التذكرة")], 1),
    ("What is dubbing?", "ما الدبلجة؟", [("Replacing voices with another language recording", "استبدال الأصوات بتسجيل بلغة أخرى"), ("Writing subtitles only", "كتابة ترجمة فقط"), ("Deleting scenes", "حذف مشاهد"), ("Changing only music", "تغيير الموسيقى فقط")], 1),
    ("Who typically oversees creative vision on a film set?", "من يشرف عادةً على الرؤية الإبداعية في موقع التصوير؟", [("Director", "مخرج"), ("Ticket seller", "بائع تذاكر"), ("Caterer only", "مقدم طعام فقط"), ("Security guard only", "حارس أمن فقط")], 1),
    ("Who often handles budgeting and hiring key crew?", "من يتولى غالبًا الميزانية وتوظيف الطاقم الرئيسي؟", [("Producer", "منتج"), ("Extra actor only", "كومبارس فقط"), ("Usher in cinema", "مرشد في السينما"), ("Popcorn vendor", "بائع فشار")], 1),
    ("What is a screenplay?", "ما السيناريو؟", [("The written script of a film", "النص المكتوب للفيلم"), ("Only the poster", "الملصق فقط"), ("Only the soundtrack album", "ألبوم الموسيقى فقط"), ("Ticket sales report", "تقرير مبيعات التذاكر")], 1),
    ("Which craft focuses on camera shots and lighting look?", "أي مهنة تركز على لقطات الكاميرا ومظهر الإضاءة؟", [("Cinematography / director of photography", "التصوير السينمائي / مدير التصوير"), ("Costume design only", "تصميم أزياء فقط"), ("Stunt driving only", "قيادة بديلة فقط"), ("Ticket printing", "طباعة تذاكر")], 1),
    ("Editing in film mainly involves what?", "المونتاج في الفيلم يعني أساسًا ماذا؟", [("Selecting and arranging shots", "اختيار ترتيب اللقطات"), ("Writing music only", "تأليف موسيقى فقط"), ("Acting only", "تمثيل فقط"), ("Selling popcorn", "بيع فشار")], 1),
    ("What is a film soundtrack?", "ما الموسيقى التصويرية؟", [("Music composed or selected for the film", "موسيقى مؤلفة أو مختارة للفيلم"), ("Only dialogue", "حوار فقط"), ("Only sound of popcorn", "صوت الفشار فقط"), ("Only credits list", "قائمة شارة فقط")], 1),
    ("Which film often marks the beginning of the MCU as a connected series (2008)?", "أي فيلم غالبًا يُعد بداية عالم مارفل المتصل (2008)؟", [("Iron Man", "آيرون مان"), ("The Dark Knight", "فارس الظلام"), ("Spider-Man (2002)", "سبايدرمان 2002"), ("X-Men (2000)", "إكس مان 2000")], 1),
    ("What is a film franchise?", "ما امتياز الأفلام؟", [("A series of related films", "سلسلة أفلام مترابطة"), ("A single short film", "فيلم قصير واحد"), ("Only a poster", "ملصق فقط"), ("A cinema building", "مبنى سينما")], 1),
]


def generate_movies(rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random(47)
    return [shuffle_preserve_pairs(qe, qa, opts, c, rng) for qe, qa, opts, c in _MOVIES_RAW]
