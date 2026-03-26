from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from quiz.data.bilingual_seed import BILINGUAL_CATEGORIES, iter_bilingual_seed
from quiz.models import Category, Question


class Command(BaseCommand):
    help = "Create categories and seed 350 bilingual questions (7×50, EN + AR)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing questions and categories before seeding.",
        )
        parser.add_argument(
            "--translate-ar",
            action="store_true",
            help="After seeding, run machine translation to fill Arabic fields (not needed for bilingual seed).",
        )
        parser.add_argument(
            "--skip-if-seeded",
            action="store_true",
            help="If questions already exist, exit successfully (for CI / Render redeploys).",
        )

    def handle(self, *args, **options):
        if Question.objects.exists() and not options["reset"]:
            if options["skip_if_seeded"]:
                self.stdout.write(
                    self.style.WARNING("Questions already exist — skipping seed (use --reset to replace).")
                )
                return
            raise CommandError(
                "Questions already exist. Run with --reset to delete and reseed, "
                "or clear the database first."
            )

        if options["reset"]:
            Question.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared questions and categories."))

        slug_to_cat: dict[str, Category] = {}
        for name_en, slug, name_ar in BILINGUAL_CATEGORIES:
            obj, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name_en, "name_ar": name_ar},
            )
            obj.name = name_en
            obj.name_ar = name_ar
            obj.save(update_fields=["name", "name_ar"])
            slug_to_cat[slug] = obj

        to_create: list[Question] = []
        for slug, q in iter_bilingual_seed():
            cat = slug_to_cat[slug]
            to_create.append(
                Question(
                    category=cat,
                    text=q["text"],
                    text_ar=q["text_ar"],
                    option1=q["option1"],
                    option2=q["option2"],
                    option3=q["option3"],
                    option4=q["option4"],
                    option1_ar=q["option1_ar"],
                    option2_ar=q["option2_ar"],
                    option3_ar=q["option3_ar"],
                    option4_ar=q["option4_ar"],
                    correct_answer=q["correct_answer"],
                )
            )
        Question.objects.bulk_create(to_create, batch_size=100)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Categories: {Category.objects.count()}, Questions: {Question.objects.count()}"
            )
        )

        if options["translate_ar"]:
            self.stdout.write(
                "Running Arabic translation… (bilingual seed already has AR; this may overwrite.)"
            )
            call_command("translate_questions_ar")
