"""
CPU opponent for vs-bot matches.

Uses binary search on [1, 100] from the bot's own guess history (hints: higher/lower).
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

BOT_USERNAME = "numbergame_bot"

User = get_user_model()


def get_bot_user():
    """Singleton-style bot account (no login; unusable password)."""
    user, created = User.objects.get_or_create(
        username=BOT_USERNAME,
        defaults={"email": "numbergame_bot@local.invalid"},
    )
    if created or user.has_usable_password():
        user.set_unusable_password()
        user.save(update_fields=["password"])
    return user


def is_bot_user(user) -> bool:
    return user is not None and getattr(user, "username", None) == BOT_USERNAME


def compute_bot_guess(game) -> int:
    """Next guess from remaining interval using previous bot guesses only."""
    from numbergame.models import Guess

    bot = get_bot_user()
    lo, hi = 1, 100
    for g in Guess.objects.filter(game=game, player=bot).order_by("timestamp"):
        if g.result == Guess.Result.HIGHER:
            lo = max(lo, g.guessed_number + 1)
        elif g.result == Guess.Result.LOWER:
            hi = min(hi, g.guessed_number - 1)
    if lo > hi:
        return max(1, min(100, lo))
    return (lo + hi) // 2
