"""DRF serializers for the number guessing API."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from numbergame.models import FriendRequest, Game, GameInvite, Profile

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = ("username", "score")


class FriendRequestSerializer(serializers.ModelSerializer):
    from_username = serializers.CharField(source="from_user.username", read_only=True)
    to_username = serializers.CharField(source="to_user.username", read_only=True)

    class Meta:
        model = FriendRequest
        fields = ("id", "from_user", "to_user", "from_username", "to_username", "status", "created_at")


class GameInviteSerializer(serializers.ModelSerializer):
    from_username = serializers.CharField(source="from_user.username", read_only=True)
    to_username = serializers.CharField(source="to_user.username", read_only=True)

    class Meta:
        model = GameInvite
        fields = (
            "id",
            "from_user",
            "to_user",
            "from_username",
            "to_username",
            "status",
            "game",
            "created_at",
        )


class GameSerializer(serializers.ModelSerializer):
    player1_username = serializers.CharField(source="player1.username", read_only=True)
    player2_username = serializers.CharField(source="player2.username", read_only=True)
    secret_setter_username = serializers.CharField(
        source="secret_setter.username", read_only=True
    )
    current_turn_username = serializers.CharField(
        source="current_turn.username", read_only=True, allow_null=True
    )
    winner_username = serializers.CharField(
        source="winner.username", read_only=True, allow_null=True
    )

    class Meta:
        model = Game
        fields = (
            "id",
            "player1",
            "player2",
            "player1_username",
            "player2_username",
            "secret_setter",
            "secret_setter_username",
            "secret_number",
            "current_turn",
            "current_turn_username",
            "status",
            "winner",
            "winner_username",
            "created_at",
            "finished_at",
        )
        read_only_fields = ("secret_number", "winner", "finished_at")
