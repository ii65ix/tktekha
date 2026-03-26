#!/usr/bin/env bash
set -euo pipefail

# تكتكها — deployment-style build (Linux/macOS/Git Bash on Windows)
# Installs dependencies, runs migrations, and seeds questions.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-smart_quiz_arena.settings}"

python manage.py migrate --noinput
python scripts/compile_locale.py
python manage.py collectstatic --noinput || true

if [[ "${SEED_ON_BUILD:-1}" == "1" ]]; then
  python manage.py seed_questions
fi

echo "Build complete. Create a superuser with: python manage.py createsuperuser"
echo "Run the app with: python manage.py runserver 0.0.0.0:8000"
