from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0002_category_name_ar_question_option1_ar_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="option1_ar",
            field=models.CharField(blank=True, default="", max_length=512),
        ),
        migrations.AlterField(
            model_name="question",
            name="option2_ar",
            field=models.CharField(blank=True, default="", max_length=512),
        ),
        migrations.AlterField(
            model_name="question",
            name="option3_ar",
            field=models.CharField(blank=True, default="", max_length=512),
        ),
        migrations.AlterField(
            model_name="question",
            name="option4_ar",
            field=models.CharField(blank=True, default="", max_length=512),
        ),
    ]
