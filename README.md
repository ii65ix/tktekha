# تكتكها

A full-stack quiz web app built with **Django**, **Bootstrap 5**, and vanilla **JavaScript**. It features authentication, seven categories (50 questions each), timed rounds (10 questions per game, **count-up elapsed timer**), **English / Arabic** UI with a navbar language switcher, score tracking, and a global leaderboard.

## Features

- User registration, login, logout, and profile with total score
- **Bilingual interface:** English and Arabic (Django i18n + `locale/ar/LC_MESSAGES/`)
- **Navbar:** switch language **English** / **العربية** (persists via cookie)
- Categories: General Knowledge, Sports, Movies, Science, Intelligence (Logic), Entertainment, Beauty & Lifestyle (English + Arabic names in the database)
- Each category: 50 multiple-choice questions stored in the database
- Each game: 10 random questions per category with a **seconds counter** (increases) and instant answer feedback
- Leaderboard sorted by total points (sum of scores across completed games)
- Django admin for categories, questions, and scores (including optional Arabic fields for each question)
- Responsive dark UI with gradients, cards, and motion (hover, fade-in, transitions); RTL layout for Arabic

## Quick start

### Requirements

- Python 3.10+

### Setup

```bash
cd /path/to/challenge.py
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**Installing packages (Windows / Git Bash):** if `pip` is not found, always use:

```bash
python -m pip install -r requirements.txt
```

Then:

```bash
python manage.py migrate
python scripts/compile_locale.py
python manage.py seed_questions
python manage.py createsuperuser
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Seeding / resetting questions

The project ships with **350** bilingual questions (**7×50**, English + Arabic). Categories: **Cars**, **Sports**, **General Knowledge**, **Geography**, **Beauty (Girls)**, **Science**, **Movies** (slugs: `cars`, `sports`, `general-knowledge`, `geography`, `beauty-lifestyle`, `science`, `movies`). Data lives under `quiz/data/bilingual_*.py` and is aggregated in `quiz/data/bilingual_seed.py`.

On a **fresh** database:

```bash
python manage.py seed_questions
```

To **replace** an existing seed (edits data or switch from an older seed):

```bash
python manage.py seed_questions --reset
```

**Warning:** `--reset` deletes existing categories and questions (and related scores via foreign keys).

If questions already exist and you run `seed_questions` without `--reset`, the command exits with an error so rows are not duplicated—use `--reset` or clear the database.

### Build script (deployment)

```bash
chmod +x build.sh
./build.sh
```

Set `SEED_ON_BUILD=0` to skip seeding on deploy if the database is already populated.

## Project layout

- `smart_quiz_arena/` — Django project settings and root URLs
- `quiz/` — Main app (`models`, `views`, `urls`, `templates`, `management/commands`)
- `static/` — `css/arena.css`, `js/quiz.js`, `img/categories/` — real thumbnails per category slug (`<slug>.jpg` / `.png` / `.webp` …; SVG fallback). See `static/img/categories/README.txt` to swap images (e.g. a makeup meme for `beauty-lifestyle`).
- `Category.category_image_relpath()` — picks the first matching `static/img/categories/<slug>.*` file for cards.
- `quiz/data/bilingual_seed.py` — wires the seven bilingual generators into one bank of 350 questions

## Arabic / English content

- **Interface strings** are translated in `locale/ar/LC_MESSAGES/django.po` (compiled to `django.mo`).
- After editing `django.po`, run: `python scripts/compile_locale.py` (uses **polib**; no GNU gettext required).

### Translating all questions and answers to Arabic

The app stores English in `text` / `option1`…`option4` and Arabic in `text_ar` / `option1_ar`…`option4_ar`. When the user selects **العربية**, the UI shows Arabic where those fields are filled.

**Automatic translation** (optional; the default seed already fills Arabic. Uses Google Translate via [deep-translator](https://pypi.org/project/deep-translator/); requires **internet**):

```bash
python -m pip install -r requirements.txt
python manage.py translate_questions_ar
```

- If the command **hangs** or is **slow**, network calls now use a **timeout**; Google is tried first, then **MyMemory** as a fallback.
- First run fills empty Arabic fields only. Use **`--force`** to overwrite existing Arabic text (including hand-written bilingual seed text).
- **`--limit N`** — translate only the first N questions (for testing).
- **`--verbosity 2`** — print each updated row.
- This can take **roughly 30–60 minutes** for all **350** questions (several network calls per question).

You can also run translation **right after seeding**:

```bash
python manage.py seed_questions --translate-ar
```

Or edit **`text_ar`** / **`option*_ar`** manually in the Django admin.

## Models

- **Category** — `name`, `name_ar`, slug
- **Question** — `text`, `text_ar`, four options + `option1_ar`…`option4_ar`, `correct_answer` (1–4), foreign key to category
- **Score** — user, points for that round (0–10), category, timestamp

## Admin

Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) after creating a superuser to manage categories, questions, and scores.

## Production notes

- Set `DEBUG = False`, configure `ALLOWED_HOSTS`, and use a strong `SECRET_KEY` environment variable
- Use PostgreSQL or another production database instead of SQLite
- Serve static files with your web server or a storage backend after `collectstatic`

## License

Use and modify freely for learning and projects.
