"""
Core game rules and score updates (used by WebSocket consumer and tests).
"""

from __future__ import annotations

from typing import Any

from django.db import transaction
from django.utils import timezone

from numbergame.models import Game, Guess, Profile


def apply_bot_game_scores(winner, loser) -> None:
    """Only the human player's Profile changes (+3 / −1); bot account has no real score."""
    from numbergame.bot import get_bot_user

    bot = get_bot_user()
    if winner.id == bot.id:
        lp, _ = Profile.objects.select_for_update().get_or_create(user_id=loser.id)
        lp.score = max(0, int(lp.score) - 1)
        lp.save(update_fields=["score"])
    elif loser.id == bot.id:
        wp, _ = Profile.objects.select_for_update().get_or_create(user_id=winner.id)
        wp.score += 3
        wp.save(update_fields=["score"])


def group_name_for_game(game_id) -> str:
    return f"guess_game_{game_id}"


@transaction.atomic
def apply_endgame_scores(winner_id: int, loser_id: int) -> None:
    """Winner +3, loser -1 (floored at 0)."""
    w_profile, _ = Profile.objects.select_for_update().get_or_create(user_id=winner_id)
    l_profile, _ = Profile.objects.select_for_update().get_or_create(user_id=loser_id)
    w_profile.score += 3
    l_profile.score = max(0, int(l_profile.score) - 1)
    w_profile.save(update_fields=["score"])
    l_profile.save(update_fields=["score"])


@transaction.atomic
def finish_game(game: Game, winner) -> dict[str, Any]:
    game.status = Game.Status.FINISHED
    game.winner = winner
    game.finished_at = timezone.now()
    game.save()
    loser = game.other_player(winner)
    if loser:
        if game.is_bot:
            apply_bot_game_scores(winner, loser)
        else:
            apply_endgame_scores(winner.id, loser.id)
    return {
        "event": "game_over",
        "winner_id": winner.id,
        "winner_username": winner.username,
        "loser_id": loser.id if loser else None,
    }


@transaction.atomic
def run_bot_turn(game_id) -> dict[str, Any] | None:
    """Execute one bot guess when it is the bot's turn (server-side)."""
    from numbergame.bot import compute_bot_guess, get_bot_user

    game = Game.objects.get(id=game_id)
    if not game.is_bot:
        return None
    bot = get_bot_user()
    if game.current_turn_id != bot.id or game.status != Game.Status.ACTIVE:
        return None
    value = compute_bot_guess(game)
    return process_guess(game, bot, value)


def process_set_secret(game: Game, user, value: int) -> dict[str, Any]:
    """Secret picker locks 1–100; second player becomes first guesser."""
    if game.status != Game.Status.WAITING_SECRET:
        return {"event": "error", "message": "Game is not waiting for a secret number."}
    if user.id != game.secret_setter_id:
        return {"event": "error", "message": "Only the designated player can set the secret."}
    if not isinstance(value, int) or not (1 <= value <= 100):
        return {"event": "error", "message": "Secret must be an integer between 1 and 100."}
    game.secret_number = value
    game.status = Game.Status.ACTIVE
    # Second player (player2) starts guessing, per spec.
    game.current_turn = game.player2
    game.save()
    return {
        "event": "secret_set",
        "game_id": str(game.id),
        "status": game.status,
        "current_turn_user_id": game.current_turn_id,
    }


def process_guess(game: Game, user, value: int) -> dict[str, Any]:
    """Validate turn, record Guess, switch turn or end game."""
    if game.status != Game.Status.ACTIVE:
        return {"event": "error", "message": "Game is not active."}
    if user.id != game.current_turn_id:
        return {"event": "error", "message": "It is not your turn to guess."}
    if not isinstance(value, int) or not (1 <= value <= 100):
        return {"event": "error", "message": "Guess must be an integer between 1 and 100."}
    secret = game.secret_number
    if secret is None:
        return {"event": "error", "message": "Secret number is not set."}

    if value == secret:
        Guess.objects.create(
            game=game,
            player=user,
            guessed_number=value,
            result=Guess.Result.CORRECT,
        )
        payload = finish_game(game, user)
        payload["guessed_number"] = value
        payload["result"] = "correct"
        return payload

    if value < secret:
        result = Guess.Result.HIGHER
        hint = "higher"
    else:
        result = Guess.Result.LOWER
        hint = "lower"

    Guess.objects.create(
        game=game,
        player=user,
        guessed_number=value,
        result=result,
    )
    other = game.other_player(user)
    game.current_turn = other
    game.save()

    return {
        "event": "receive_result",
        "result": hint,
        "guessed_number": value,
        "secret_relative": hint,
        "next_event": "switch_turn",
        "current_turn_user_id": other.id,
        "current_turn_username": other.username,
    }
