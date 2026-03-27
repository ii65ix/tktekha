from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from collections import defaultdict

from quiz.data.bilingual_seed import (
    BILINGUAL_CATEGORIES,
    EXPECTED_COUNTS,
    iter_bilingual_seed,
)
from quiz.models import Category, Question


class Command(BaseCommand):
    help = "Create categories and seed bilingual questions (EN + AR)."

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
        # If we're deploying repeatedly (e.g. Render), we don't want duplicates.
        # With --skip-if-seeded, we only fill missing/short categories.
        if options["reset"]:
            Question.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared questions and categories."))
        elif Question.objects.exists() and not options["reset"]:
            if not options["skip_if_seeded"]:
                raise CommandError(
                    "Questions already exist. Run with --reset to delete and reseed, "
                    "or clear the database first."
                )

        slug_to_cat: dict[str, Category] = {}
        for name_en, slug, name_ar in BILINGUAL_CATEGORIES:
            obj, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name_en, "name_ar": name_ar},
            )
            # Keep category names in sync (especially for Arabic display).
            obj.name = name_en
            obj.name_ar = name_ar
            obj.save(update_fields=["name", "name_ar"])
            slug_to_cat[slug] = obj

        # Build the full seed bank once.
        bank: dict[str, list[dict]] = defaultdict(list)
        for slug, q in iter_bilingual_seed():
            bank[slug].append(q)

        def seed_slug(slug: str) -> int:
            cat = slug_to_cat[slug]
            Question.objects.filter(category=cat).delete()
            to_create = [
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
                for q in bank[slug]
            ]
            Question.objects.bulk_create(to_create, batch_size=100)
            return len(to_create)

        if not Question.objects.exists() or options["reset"]:
            # Fresh DB: seed everything.
            for slug in EXPECTED_COUNTS.keys():
                seed_slug(slug)
        else:
            # DB exists: only seed categories that are missing/short.
            seeded_any = False
            for slug, expected in EXPECTED_COUNTS.items():
                cat = slug_to_cat[slug]
                existing = Question.objects.filter(category=cat).count()
                if existing < expected:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Seeding missing '{slug}': existing {existing}, expected {expected}"
                        )
                    )
                    seed_slug(slug)
                    seeded_any = True
            if not seeded_any and options["skip_if_seeded"]:
                self.stdout.write(
                    self.style.SUCCESS("All categories already seeded — nothing to do.")
                )
                return

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
