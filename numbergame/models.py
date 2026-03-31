"""
Online 1v1 number guessing game models.

Game flow:
- One player sets a secret in [1, 100]; the other starts guessing (per product spec).
- After each wrong guess, players alternate; server replies higher / lower / correct.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class Profile(models.Model):
    """Persistent score for the guessing game (separate from quiz Score rows)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="numbergame_profile",
    )
    score = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-score"]

    def __str__(self) -> str:
        return f"{self.user.username} — {self.score} pts"


class FriendRequest(models.Model):
    """Friend link by username; must be accepted before sending game invites."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friend_requests_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friend_requests_received",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"],
                name="unique_friend_request_pair",
            ),
            models.CheckConstraint(
                condition=~Q(from_user_id=F("to_user_id")),
                name="friend_request_not_self",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.from_user} → {self.to_user} ({self.status})"


class Friendship(models.Model):
    """Accepted symmetric friendship (one row per pair, user_id < friend_id)."""

    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_edges_a",
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_edges_b",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_a", "user_b"],
                name="unique_friendship_pair",
            ),
            models.CheckConstraint(
                condition=Q(user_a_id__lt=F("user_b_id")),
                name="friendship_ordered_ids",
            ),
        ]

    @classmethod
    def add_pair(cls, u1, u2) -> Friendship:
        a_id, b_id = sorted([u1.id, u2.id])
        ua = u1 if u1.id == a_id else u2
        ub = u2 if u2.id == b_id else u1
        return cls.objects.get_or_create(user_a=ua, user_b=ub)[0]


class Game(models.Model):
    """A single 1v1 match."""

    class Status(models.TextChoices):
        WAITING_SECRET = "waiting_secret", "Waiting for secret number"
        ACTIVE = "active", "Active"
        FINISHED = "finished", "Finished"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guess_games_as_p1",
    )
    player2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guess_games_as_p2",
    )
    # Who must pick the secret (typically inviter / player1).
    secret_setter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="games_where_sets_secret",
    )
    secret_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="1–100, set over WebSocket before ACTIVE.",
    )
    # Whose turn it is to *guess* (not to set secret).
    current_turn = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guess_games_current_turn",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.WAITING_SECRET,
        db_index=True,
    )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="guess_games_won",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def other_player(self, user):
        if user.id == self.player1_id:
            return self.player2
        if user.id == self.player2_id:
            return self.player1
        return None


class GameInvite(models.Model):
    """Invite a friend to a new guessing match."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_invites_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_invites_received",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    game = models.OneToOneField(
        Game,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_invite",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class Guess(models.Model):
    """One guess attempt in a game."""

    class Result(models.TextChoices):
        HIGHER = "higher", "higher"  # secret is higher than guess
        LOWER = "lower", "lower"  # secret is lower than guess
        CORRECT = "correct", "correct"

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="guesses")
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guess_moves",
    )
    guessed_number = models.PositiveSmallIntegerField()
    result = models.CharField(max_length=16, choices=Result.choices)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["timestamp"]
