from django.conf import settings
from django.contrib.staticfiles import finders
from django.db import models
from django.utils.text import slugify

_CATEGORY_THUMB_EXTS: tuple[str, ...] = (
    ".webp",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
)


class Category(models.Model):
    name = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120, blank=True, default="")
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def display_name(self):
        from django.utils import translation

        if translation.get_language().startswith("ar") and self.name_ar:
            return self.name_ar
        return self.name

    def category_image_relpath(self) -> str:
        """Path under static/ for category card image (raster preferred, then SVG)."""
        base = f"img/categories/{self.slug}"
        for ext in _CATEGORY_THUMB_EXTS:
            rel = f"{base}{ext}"
            if finders.find(rel):
                return rel
        return f"{base}.svg"


class Question(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    text_ar = models.TextField(blank=True, default="")
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    option1_ar = models.CharField(max_length=512, blank=True, default="")
    option2_ar = models.CharField(max_length=512, blank=True, default="")
    option3_ar = models.CharField(max_length=512, blank=True, default="")
    option4_ar = models.CharField(max_length=512, blank=True, default="")
    correct_answer = models.PositiveSmallIntegerField(
        help_text="1–4 for which option is correct"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text[:60] + ("…" if len(self.text) > 60 else "")

    def text_localized(self):
        from django.utils import translation

        if translation.get_language().startswith("ar") and self.text_ar:
            return self.text_ar
        return self.text

    def option_localized(self, n: int) -> str:
        from django.utils import translation

        if translation.get_language().startswith("ar"):
            ar = getattr(self, f"option{n}_ar", None) or ""
            if ar:
                return ar
        return getattr(self, f"option{n}")

    def correct_option_localized(self) -> str:
        return self.option_localized(self.correct_answer)


class Score(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_scores"
    )
    score = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="scores"
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} — {self.score} ({self.category.name})"
