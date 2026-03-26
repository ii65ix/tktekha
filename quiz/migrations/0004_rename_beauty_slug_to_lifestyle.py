# Generated manually — align Category slug with URLs used before bilingual seed.

from django.db import migrations


def forwards(apps, schema_editor):
    Category = apps.get_model("quiz", "Category")
    Category.objects.filter(slug="beauty-girls").update(slug="beauty-lifestyle")


def backwards(apps, schema_editor):
    Category = apps.get_model("quiz", "Category")
    Category.objects.filter(slug="beauty-lifestyle").update(slug="beauty-girls")


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0003_alter_question_option_ar_lengths"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
