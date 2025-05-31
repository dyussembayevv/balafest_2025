from django.contrib import admin
from .models import Participant, Game, GameCompletion, GamePlacement


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    ordering = ['name']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_place_points', 'second_place_points', 'third_place_points', 'age_group')
    list_filter = ('age_group',)
    search_fields = ('name',)

@admin.register(GameCompletion)
class GameCompletionAdmin(admin.ModelAdmin):
    list_display = ('participant', 'game', 'completed')
    list_filter = ('completed',)

admin.site.register(GamePlacement)
