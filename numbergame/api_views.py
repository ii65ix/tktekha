"""REST API: friends, invites, score, token for mobile clients."""

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from numbergame.models import FriendRequest, Friendship, Game, GameInvite, Profile
from numbergame.serializers import (
    FriendRequestSerializer,
    GameInviteSerializer,
    GameSerializer,
    ProfileSerializer,
    UserBriefSerializer,
)

User = get_user_model()


def _friends_queryset(user):
    return Friendship.objects.filter(Q(user_a=user) | Q(user_b=user))


def _friend_users(user):
    friends = []
    for row in _friends_queryset(user):
        other = row.user_b if row.user_a_id == user.id else row.user_a
        friends.append(other)
    return friends


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_score(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return Response(ProfileSerializer(profile).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    """Return DRF token for React Native / API clients (use with Authorization: Token <key>)."""
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(
            {"detail": "username and password required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = authenticate(request, username=username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user_id": user.id, "username": user.username})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def friend_request_create(request):
    """Body: { \"username\": \"other\" }"""
    uname = (request.data.get("username") or "").strip()
    if not uname:
        return Response({"detail": "username required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        other = User.objects.get(username__iexact=uname)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    if other.id == request.user.id:
        return Response({"detail": "Cannot add yourself"}, status=status.HTTP_400_BAD_REQUEST)
    fr = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=other,
        status=FriendRequest.Status.PENDING,
    ).first()
    if fr:
        return Response(FriendRequestSerializer(fr).data, status=status.HTTP_200_OK)
    fr = FriendRequest.objects.create(
        from_user=request.user,
        to_user=other,
        status=FriendRequest.Status.PENDING,
    )
    return Response(FriendRequestSerializer(fr).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friend_request_list(request):
    incoming = FriendRequest.objects.filter(
        to_user=request.user, status=FriendRequest.Status.PENDING
    )
    outgoing = FriendRequest.objects.filter(
        from_user=request.user, status=FriendRequest.Status.PENDING
    )
    return Response(
        {
            "incoming": FriendRequestSerializer(incoming, many=True).data,
            "outgoing": FriendRequestSerializer(outgoing, many=True).data,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def friend_request_accept(request, pk):
    fr = FriendRequest.objects.filter(
        pk=pk, to_user=request.user, status=FriendRequest.Status.PENDING
    ).first()
    if not fr:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    fr.status = FriendRequest.Status.ACCEPTED
    fr.save(update_fields=["status", "updated_at"])
    Friendship.add_pair(fr.from_user, fr.to_user)
    return Response({"detail": "accepted"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def friend_request_reject(request, pk):
    fr = FriendRequest.objects.filter(
        pk=pk, to_user=request.user, status=FriendRequest.Status.PENDING
    ).first()
    if not fr:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    fr.status = FriendRequest.Status.REJECTED
    fr.save(update_fields=["status", "updated_at"])
    return Response({"detail": "rejected"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friends_list(request):
    users = _friend_users(request.user)
    return Response(UserBriefSerializer(users, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def game_invite_create(request):
    """Body: { \"to_user_id\": 2 } — must be an accepted friend."""
    try:
        uid = int(request.data.get("to_user_id"))
    except (TypeError, ValueError):
        return Response({"detail": "to_user_id required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        other = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    if other.id == request.user.id:
        return Response({"detail": "Invalid target"}, status=status.HTTP_400_BAD_REQUEST)
    if other not in _friend_users(request.user):
        return Response(
            {"detail": "You can only invite friends (accept friend request first)."},
            status=status.HTTP_403_FORBIDDEN,
        )
    inv = GameInvite.objects.filter(
        from_user=request.user,
        to_user=other,
        status=GameInvite.Status.PENDING,
    ).first()
    if inv:
        return Response(GameInviteSerializer(inv).data, status=status.HTTP_200_OK)
    inv = GameInvite.objects.create(
        from_user=request.user,
        to_user=other,
        status=GameInvite.Status.PENDING,
    )
    return Response(GameInviteSerializer(inv).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def game_invite_accept(request, pk):
    invite = GameInvite.objects.filter(
        pk=pk, to_user=request.user, status=GameInvite.Status.PENDING
    ).first()
    if not invite:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    game = Game.objects.create(
        player1=invite.from_user,
        player2=invite.to_user,
        secret_setter=invite.from_user,
        status=Game.Status.WAITING_SECRET,
        current_turn=None,
    )
    invite.game = game
    invite.status = GameInvite.Status.ACCEPTED
    invite.save(update_fields=["game", "status", "updated_at"])
    return Response({"game_id": str(game.id), "game": GameSerializer(game).data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def game_invite_reject(request, pk):
    invite = GameInvite.objects.filter(
        pk=pk, to_user=request.user, status=GameInvite.Status.PENDING
    ).first()
    if not invite:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    invite.status = GameInvite.Status.REJECTED
    invite.save(update_fields=["status", "updated_at"])
    return Response({"detail": "rejected"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def game_detail(request, game_id):
    game = Game.objects.filter(pk=game_id).first()
    if not game:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.user.id not in (game.player1_id, game.player2_id):
        return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    data = GameSerializer(game).data
    # Hide secret from API until game finished (optional policy).
    if game.status != Game.Status.FINISHED:
        data["secret_number"] = None
    return Response(data)
