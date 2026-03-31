"""
WebSocket consumer for realtime 1v1 guessing.

Client JSON messages:
- {"type": "set_secret", "value": <1-100>}  — only secret_setter while status is waiting_secret
- {"type": "send_guess", "value": <1-100>} — only current_turn while active

Server pushes JSON events (same shape for both players):
- connect, secret_set, receive_result, switch_turn (via payload fields), game_over, error
"""

from __future__ import annotations

import uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from numbergame.models import Game
from numbergame.services import group_name_for_game, process_guess, process_set_secret

User = get_user_model()


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        raw = self.scope["url_route"]["kwargs"]["game_id"]
        try:
            self.game_uuid = uuid.UUID(str(raw))
        except ValueError:
            await self.close(code=4400)
            return

        self.game_id = str(self.game_uuid)
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close(code=4401)
            return

        game = await self.fetch_game()
        if not game:
            await self.close(code=4404)
            return
        if user.id not in (game.player1_id, game.player2_id):
            await self.close(code=4403)
            return

        self.group = group_name_for_game(self.game_id)
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
        await self.send_json(
            {
                "event": "connect",
                "game_id": self.game_id,
                "user_id": user.id,
                "status": game.status,
            }
        )

    async def disconnect(self, code):
        if hasattr(self, "group"):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        user = self.scope["user"]
        if not user.is_authenticated:
            return
        msg_type = (content or {}).get("type")
        try:
            value = int((content or {}).get("value"))
        except (TypeError, ValueError):
            await self.send_json({"event": "error", "message": "Invalid or missing integer value."})
            return

        if msg_type == "set_secret":
            result = await self.run_set_secret(user.id, value)
        elif msg_type == "send_guess":
            result = await self.run_guess(user.id, value)
        else:
            await self.send_json(
                {
                    "event": "error",
                    "message": "Unknown type. Use set_secret or send_guess.",
                }
            )
            return

        await self.broadcast(result)

    async def guess_broadcast(self, event):
        """Handler for group_send type 'guess_broadcast'."""
        await self.send_json(event["payload"])

    @database_sync_to_async
    def fetch_game(self):
        try:
            return Game.objects.select_related(
                "player1", "player2", "secret_setter", "current_turn", "winner"
            ).get(id=self.game_uuid)
        except Game.DoesNotExist:
            return None

    @database_sync_to_async
    def run_set_secret(self, user_id: int, value: int) -> dict:
        game = Game.objects.get(id=self.game_uuid)
        user = User.objects.get(pk=user_id)
        return process_set_secret(game, user, value)

    @database_sync_to_async
    def run_guess(self, user_id: int, value: int) -> dict:
        game = Game.objects.get(id=self.game_uuid)
        user = User.objects.get(pk=user_id)
        return process_guess(game, user, value)

    async def broadcast(self, payload: dict) -> None:
        if payload.get("event") == "error":
            await self.send_json(payload)
            return
        await self.channel_layer.group_send(
            self.group,
            {"type": "guess.broadcast", "payload": payload},
        )
