from django.contrib import admin
from .models import Participant

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'calculated_points')
    ordering = ['name']

    def calculated_points(self, obj):
        from .models import GameCompletion
        return sum(gc.game.points for gc in GameCompletion.objects.filter(participant=obj, completed=True))

    calculated_points.short_description = 'Points'
