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

from numbergame.models import Profile as NumbergameProfile

from .forms import ArenaLoginForm, RegisterForm
from .models import Category, Question, Score

SESSION_QUIZ_KEY = "smart_quiz_arena_quiz"
TMASIHA_SLUG = "tmasih-abudka"
TMASIHA_MULTIPLIER = 2  # points are different for the gateway challenge.
TMASIHA_TEAM_MODE = "tmasih_teams"


def redirect_beauty_girls_slug(request):
    """Old bilingual seed used slug beauty-girls; canonical URL is beauty-lifestyle."""
    return redirect("start_quiz", slug="beauty-lifestyle")


def home(request):
    categories = Category.objects.exclude(slug=TMASIHA_SLUG)[:7]
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
        {"categories": Category.objects.exclude(slug=TMASIHA_SLUG)},
    )


@login_required
def start_quiz(request, slug):
    if slug == TMASIHA_SLUG:
        return redirect("tmasih_team_setup")
    category = get_object_or_404(Category, slug=slug)
    pool = list(
        Question.objects.filter(category=category).values_list("id", flat=True)
    )
    round_size = 10
    if len(pool) < round_size:
        messages.error(
            request,
            _("Not enough questions in this category yet. Please try another."),
        )
        return redirect("categories")
    random.shuffle(pool)
    chosen = pool[:round_size]
    request.session[SESSION_QUIZ_KEY] = {
        "category_id": category.id,
        "question_ids": chosen,
        "index": 0,
        "correct": 0,
        "results": [],
    }
    return redirect("quiz_play")


def _tmasih_round_size() -> int:
    return 12


@login_required
def tmasih_team_setup(request):
    """Two-team turn-based match for Tamasih Abudka (same device)."""
    category = get_object_or_404(Category, slug=TMASIHA_SLUG)
    pool = list(
        Question.objects.filter(category=category).values_list("id", flat=True)
    )
    n = _tmasih_round_size()
    if len(pool) < n:
        messages.error(
            request,
            _("Not enough questions in this category yet. Please try another."),
        )
        return redirect("categories")

    if request.method == "POST":
        raw1 = (request.POST.get("team1_name") or "").strip()
        raw2 = (request.POST.get("team2_name") or "").strip()
        name1 = (raw1[:48] if raw1 else str(_("Team 1")))
        name2 = (raw2[:48] if raw2 else str(_("Team 2")))
        random.shuffle(pool)
        chosen = pool[:n]
        request.session[SESSION_QUIZ_KEY] = {
            "category_id": category.id,
            "question_ids": chosen,
            "index": 0,
            "correct": 0,
            "results": [],
            "mode": TMASIHA_TEAM_MODE,
            "team_names": [name1, name2],
            "team_scores": [0, 0],
        }
        request.session.modified = True
        return redirect("quiz_play")

    return render(
        request,
        "quiz/tmasih_team_setup.html",
        {
            "category": category,
            "round_questions": n,
        },
    )


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
            if data.get("mode") == TMASIHA_TEAM_MODE:
                ts = data.get("team_scores") or [0, 0]
                team_idx = idx % 2
                if len(ts) > team_idx:
                    ts[team_idx] = ts[team_idx] + 1
                    data["team_scores"] = ts

        result_row = {
            "question_id": question.id,
            "selected": selected,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
        }
        if data.get("mode") == TMASIHA_TEAM_MODE:
            result_row["team_index"] = idx % 2
        data["results"].append(result_row)
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
            if data.get("mode") == TMASIHA_TEAM_MODE:
                payload["team_scores"] = data.get("team_scores") or [0, 0]
                payload["team_names"] = data.get("team_names") or []
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
    ctx = {
        "category": category,
        "question": question,
        "question_num": idx + 1,
        "total_questions": total_q,
        "progress": progress,
        "options": options,
    }
    if data.get("mode") == TMASIHA_TEAM_MODE:
        names = data.get("team_names") or [str(_("Team 1")), str(_("Team 2"))]
        scores = data.get("team_scores") or [0, 0]
        turn = idx % 2
        ctx["tmasih_team_mode"] = True
        ctx["team_names"] = names
        ctx["team_scores"] = scores
        ctx["active_team_index"] = turn
        ctx["active_team_name"] = names[turn] if turn < len(names) else ""
    return render(request, "quiz/quiz.html", ctx)


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

    points = final
    max_points = len(ids)
    if category.slug == TMASIHA_SLUG:
        points = final * TMASIHA_MULTIPLIER
        max_points = len(ids) * TMASIHA_MULTIPLIER

    Score.objects.create(user=request.user, score=points, category=category)
    team_mode = data.get("mode") == TMASIHA_TEAM_MODE
    team_names = data.get("team_names") or []
    team_scores = data.get("team_scores") or [0, 0]
    winner_index = None
    winner_name = None
    is_tie = False
    if team_mode and len(team_scores) >= 2:
        if team_scores[0] > team_scores[1]:
            winner_index = 0
        elif team_scores[1] > team_scores[0]:
            winner_index = 1
        else:
            is_tie = True
        if winner_index is not None and winner_index < len(team_names):
            winner_name = team_names[winner_index]

    details = []
    for i, rid in enumerate(ids):
        q = Question.objects.get(pk=rid)
        r = data["results"][i] if i < len(data.get("results", [])) else {}
        row = {
            "question": q,
            "selected": r.get("selected"),
            "is_correct": r.get("is_correct", False),
        }
        if team_mode:
            ti = r.get("team_index")
            if ti is not None and ti < len(team_names):
                row["team_label"] = team_names[ti]
        details.append(row)

    del request.session[SESSION_QUIZ_KEY]
    request.session.modified = True

    total_points = (
        Score.objects.filter(user=request.user).aggregate(s=Sum("score"))["s"] or 0
    )

    play_again_url = (
        reverse("tmasih_team_setup")
        if category.slug == TMASIHA_SLUG
        else reverse("start_quiz", kwargs={"slug": category.slug})
    )

    return render(
        request,
        "quiz/result.html",
        {
            "category": category,
            "score": points,
            "max_score": max_points,
            "details": details,
            "total_points": total_points,
            "tmasih_team_mode": team_mode,
            "team_names": team_names,
            "team_scores": team_scores,
            "winner_index": winner_index,
            "winner_name": winner_name,
            "is_tie": is_tie,
            "play_again_url": play_again_url,
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
    ng_profile, _ = NumbergameProfile.objects.get_or_create(user=user)
    return render(
        request,
        "quiz/profile.html",
        {
            "total_score": total,
            "recent": recent,
            "numbergame_score": ng_profile.score,
        },
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
