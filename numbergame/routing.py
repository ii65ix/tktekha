from django.urls import re_path

from numbergame.consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<game_id>[0-9a-fA-F-]{36})/$", GameConsumer.as_asgi()),
]
