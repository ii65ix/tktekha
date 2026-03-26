from django.contrib import admin

from .models import Category, Question, Score


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_ar", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "name_ar", "slug")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_short", "category", "correct_answer")
    list_filter = ("category",)
    search_fields = ("text", "text_ar", "option1", "option2", "option3", "option4")
    fieldsets = (
        (None, {"fields": ("category", "correct_answer")}),
        ("English", {"fields": ("text", "option1", "option2", "option3", "option4")}),
        ("Arabic", {"fields": ("text_ar", "option1_ar", "option2_ar", "option3_ar", "option4_ar")}),
    )

    @staticmethod
    def text_short(obj):
        return (obj.text[:50] + "…") if len(obj.text) > 50 else obj.text


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "category", "date")
    list_filter = ("category", "date")
    search_fields = ("user__username",)
