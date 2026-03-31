"""
ASGI config: HTTP (Django) + WebSocket (Channels) for realtime guessing games.

For production, run with Daphne or Uvicorn, not Gunicorn (WS requires ASGI).
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_quiz_arena.settings")

django_asgi_app = get_asgi_application()

from numbergame.middleware import TokenQueryAuthMiddleware  # noqa: E402
from numbergame.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                TokenQueryAuthMiddleware(
                    URLRouter(websocket_urlpatterns),
                )
            )
        ),
    }
)
