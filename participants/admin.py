from django.contrib import admin
from .models import Participant

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    search_fields = ['name', 'uuid']
    ordering = ['-points']
    list_display = ('uuid', 'name', 'points')
