"""Allow WebSocket auth via ?token=<DRF token> for React Native / API clients."""

from __future__ import annotations

from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def _user_for_token(key: str):
    try:
        return Token.objects.select_related("user").get(key=key).user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenQueryAuthMiddleware:
    """Runs *inside* AuthMiddlewareStack so session user is set first; token overrides."""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "websocket":
            qs = parse_qs(scope.get("query_string", b"").decode())
            token_key = (qs.get("token") or [None])[0]
            if token_key:
                user = await _user_for_token(token_key)
                if user.is_authenticated:
                    scope["user"] = user
        return await self.inner(scope, receive, send)
