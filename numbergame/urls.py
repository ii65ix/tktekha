from django.urls import path

from numbergame import api_views, web_views

urlpatterns = [
    path("numbergame/", web_views.lobby, name="numbergame_lobby"),
    path(
        "numbergame/game/<uuid:game_id>/",
        web_views.game_room,
        name="numbergame_room",
    ),
    # --- REST API (session or Token auth) ---
    path("api/numbergame/auth/token/", api_views.obtain_auth_token, name="ng_obtain_token"),
    path("api/numbergame/me/score/", api_views.my_score, name="ng_my_score"),
    path("api/numbergame/friends/", api_views.friends_list, name="ng_friends_list"),
    path(
        "api/numbergame/friends/request/",
        api_views.friend_request_create,
        name="ng_friend_request_create",
    ),
    path(
        "api/numbergame/friends/request/<int:pk>/accept/",
        api_views.friend_request_accept,
    ),
    path(
        "api/numbergame/friends/request/<int:pk>/reject/",
        api_views.friend_request_reject,
    ),
    path("api/numbergame/friends/requests/", api_views.friend_request_list),
    path("api/numbergame/invites/", api_views.game_invite_create, name="ng_game_invite_create"),
    path(
        "api/numbergame/invites/<int:pk>/accept/",
        api_views.game_invite_accept,
    ),
    path(
        "api/numbergame/invites/<int:pk>/reject/",
        api_views.game_invite_reject,
    ),
    path("api/numbergame/games/<uuid:game_id>/", api_views.game_detail),
]
