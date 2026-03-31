from django.contrib import admin

from numbergame.models import FriendRequest, Friendship, Game, GameInvite, Guess, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "score")
    search_fields = ("user__username",)


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "status", "created_at")
    list_filter = ("status",)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("user_a", "user_b", "created_at")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "player1",
        "player2",
        "is_bot",
        "status",
        "secret_setter",
        "current_turn",
        "winner",
        "created_at",
    )
    list_filter = ("status", "is_bot")


@admin.register(GameInvite)
class GameInviteAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "status", "game", "created_at")
    list_filter = ("status",)


@admin.register(Guess)
class GuessAdmin(admin.ModelAdmin):
    list_display = ("game", "player", "guessed_number", "result", "timestamp")
