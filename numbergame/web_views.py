"""Browser UI for lobby + game room (WebSocket client)."""

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from numbergame.api_views import _friend_users
from numbergame.models import FriendRequest, Game, GameInvite, Profile


@login_required
def lobby(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    friends = _friend_users(request.user)
    incoming_fr = FriendRequest.objects.filter(
        to_user=request.user, status=FriendRequest.Status.PENDING
    ).select_related("from_user")
    outgoing_fr = FriendRequest.objects.filter(
        from_user=request.user, status=FriendRequest.Status.PENDING
    ).select_related("to_user")
    incoming_inv = GameInvite.objects.filter(
        to_user=request.user, status=GameInvite.Status.PENDING
    ).select_related("from_user")
    outgoing_inv = GameInvite.objects.filter(
        from_user=request.user, status=GameInvite.Status.PENDING
    ).select_related("to_user")
    active_games = (
        Game.objects.filter(
            Q(player1=request.user) | Q(player2=request.user),
            status__in=[Game.Status.WAITING_SECRET, Game.Status.ACTIVE],
        )
        .select_related("player1", "player2")
        .order_by("-updated_at")[:10]
    )

    return render(
        request,
        "numbergame/lobby.html",
        {
            "profile": profile,
            "friends": friends,
            "incoming_fr": incoming_fr,
            "outgoing_fr": outgoing_fr,
            "incoming_inv": incoming_inv,
            "outgoing_inv": outgoing_inv,
            "active_games": active_games,
        },
    )


@login_required
def game_room(request, game_id):
    game = get_object_or_404(
        Game.objects.select_related("player1", "player2", "secret_setter", "current_turn"),
        pk=game_id,
    )
    if request.user.id not in (game.player1_id, game.player2_id):
        return redirect("numbergame_lobby")
    ws_scheme = "wss" if request.is_secure() else "ws"
    host = request.get_host()
    ws_url = f"{ws_scheme}://{host}/ws/game/{game.id}/"
    return render(
        request,
        "numbergame/game_room.html",
        {
            "game": game,
            "ws_url": ws_url,
            "is_secret_setter": request.user.id == game.secret_setter_id,
        },
    )
