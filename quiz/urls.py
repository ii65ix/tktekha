from django.urls import path

from . import views
from .views import ArenaLoginView, ArenaLogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.categories_list, name="categories"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("register/", views.register, name="register"),
    path("login/", ArenaLoginView.as_view(), name="login"),
    path("logout/", ArenaLogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path(
        "quiz/beauty-girls/start/",
        views.redirect_beauty_girls_slug,
        name="redirect_beauty_girls",
    ),
    path(
        "quiz/tmasih-abudka/teams/",
        views.tmasih_team_setup,
        name="tmasih_team_setup",
    ),
    path("quiz/<slug:slug>/start/", views.start_quiz, name="start_quiz"),
    path("quiz/play/", views.quiz_play, name="quiz_play"),
    path("result/", views.quiz_result, name="quiz_result"),
]
