import json
import random

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from .forms import ArenaLoginForm, RegisterForm
from .models import Category, Question, Score

SESSION_QUIZ_KEY = "smart_quiz_arena_quiz"


def redirect_beauty_girls_slug(request):
    """Old bilingual seed used slug beauty-girls; canonical URL is beauty-lifestyle."""
    return redirect("start_quiz", slug="beauty-lifestyle")


def home(request):
    categories = Category.objects.all()[:7]
    top = (
        Score.objects.values("user__username")
        .annotate(total=Sum("score"))
        .order_by("-total")[:5]
    )
    return render(
        request,
        "quiz/home.html",
        {"categories": categories, "top_preview": top},
    )


def categories_list(request):
    return render(
        request,
        "quiz/categories.html",
        {"categories": Category.objects.all()},
    )


@login_required
def start_quiz(request, slug):
    category = get_object_or_404(Category, slug=slug)
    pool = list(
        Question.objects.filter(category=category).values_list("id", flat=True)
    )
    if len(pool) < 10:
        messages.error(
            request,
            _("Not enough questions in this category yet. Please try another."),
        )
        return redirect("categories")
    random.shuffle(pool)
    chosen = pool[:10]
    request.session[SESSION_QUIZ_KEY] = {
        "category_id": category.id,
        "question_ids": chosen,
        "index": 0,
        "correct": 0,
        "results": [],
    }
    return redirect("quiz_play")


@login_required
def quiz_play(request):
    data = request.session.get(SESSION_QUIZ_KEY)
    if not data:
        messages.warning(request, _("Start a quiz from the categories page."))
        return redirect("categories")

    category = get_object_or_404(Category, id=data["category_id"])
    ids = data["question_ids"]
    idx = data["index"]

    if idx >= len(ids):
        return redirect("quiz_result")

    question = get_object_or_404(Question, id=ids[idx])
    total_q = len(ids)
    progress = idx / total_q * 100

    if request.method == "POST":
        body = {}
        ct = request.content_type or ""
        if ct.startswith("application/json"):
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                body = {}
        choice_raw = request.POST.get("choice")
        if choice_raw is None:
            choice_raw = body.get("choice")
        timed_out = (
            request.POST.get("timed_out") == "1"
            or body.get("timed_out") is True
        )

        if timed_out:
            selected = None
            is_correct = False
        elif choice_raw is None:
            selected = None
            is_correct = False
        else:
            try:
                selected = int(choice_raw)
            except (TypeError, ValueError):
                selected = None
            is_correct = (
                selected is not None
                and 1 <= selected <= 4
                and selected == question.correct_answer
            )

        if is_correct:
            data["correct"] = data.get("correct", 0) + 1

        data["results"].append(
            {
                "question_id": question.id,
                "selected": selected,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
            }
        )
        data["index"] = idx + 1
        request.session[SESSION_QUIZ_KEY] = data
        request.session.modified = True

        if ct.startswith("application/json"):
            next_idx = data["index"]
            done = next_idx >= len(ids)
            payload = {
                "ok": True,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "score_so_far": data["correct"],
                "done": done,
            }
            if done:
                payload["redirect"] = request.build_absolute_uri(
                    reverse("quiz_result")
                )
            return JsonResponse(payload)

        return redirect("quiz_play")

    options = [
        (1, question.option_localized(1)),
        (2, question.option_localized(2)),
        (3, question.option_localized(3)),
        (4, question.option_localized(4)),
    ]
    return render(
        request,
        "quiz/quiz.html",
        {
            "category": category,
            "question": question,
            "question_num": idx + 1,
            "total_questions": total_q,
            "progress": progress,
            "options": options,
        },
    )


@login_required
def quiz_result(request):
    data = request.session.get(SESSION_QUIZ_KEY)
    if not data:
        return redirect("categories")

    category = get_object_or_404(Category, id=data["category_id"])
    final = data.get("correct", 0)
    ids = data["question_ids"]
    if data.get("index", 0) < len(ids):
        messages.info(request, _("Finish all questions first."))
        return redirect("quiz_play")

    Score.objects.create(user=request.user, score=final, category=category)
    details = []
    for i, rid in enumerate(ids):
        q = Question.objects.get(pk=rid)
        r = data["results"][i] if i < len(data.get("results", [])) else {}
        details.append(
            {
                "question": q,
                "selected": r.get("selected"),
                "is_correct": r.get("is_correct", False),
            }
        )

    del request.session[SESSION_QUIZ_KEY]
    request.session.modified = True

    total_points = (
        Score.objects.filter(user=request.user).aggregate(s=Sum("score"))["s"] or 0
    )

    return render(
        request,
        "quiz/result.html",
        {
            "category": category,
            "score": final,
            "max_score": len(ids),
            "details": details,
            "total_points": total_points,
        },
    )


def leaderboard(request):
    rows = (
        Score.objects.values("user__username")
        .annotate(total=Sum("score"))
        .order_by("-total")[:50]
    )
    return render(request, "quiz/leaderboard.html", {"rows": rows})


@login_required
def profile(request):
    user = request.user
    total = Score.objects.filter(user=user).aggregate(s=Sum("score"))["s"] or 0
    recent = Score.objects.filter(user=user).select_related("category")[:15]
    return render(
        request,
        "quiz/profile.html",
        {"total_score": total, "recent": recent},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Welcome to تكتكها!"))
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "quiz/register.html", {"form": form})


class ArenaLoginView(LoginView):
    template_name = "quiz/login.html"
    form_class = ArenaLoginForm
    redirect_authenticated_user = True


class ArenaLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]
