import time

from django.core.management.base import BaseCommand

from quiz.models import Question
from quiz.translation_utils import translate_question_fields


class Command(BaseCommand):
    help = (
        "Fill text_ar and option1_ar–option4_ar for all questions using "
        "English→Arabic machine translation (requires network)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing Arabic text.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Only process the first N questions (0 = all).",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=0.0,
            help="Extra seconds to wait after each question (in addition to internal pacing).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        limit = options["limit"]
        delay = max(0.0, options["delay"])
        verbosity = int(options.get("verbosity", 1))

        qs = Question.objects.order_by("id")
        if limit > 0:
            qs = qs[:limit]

        examined = 0
        saved = 0
        try:
            for q in qs:
                examined += 1
                fields = translate_question_fields(q, force=force)
                if fields:
                    q.save(update_fields=fields)
                    saved += 1
                    if verbosity >= 2:
                        self.stdout.write(
                            self.style.SUCCESS(f"#{q.pk} → {', '.join(fields)}")
                        )
                elif verbosity >= 2:
                    self.stdout.write(f"#{q.pk} skipped (already filled or failed)")
                time.sleep(delay)
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING(
                    "\nStopped by user. Already-saved questions are kept in the database."
                )
            )
            raise

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished. Saved Arabic for {saved} question(s), examined {examined}."
            )
        )
