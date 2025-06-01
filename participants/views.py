from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Participant, Game

def index(request):
    top_participants = Participant.objects.order_by('-points')[:10]  # or other sorting field
    return render(request, 'index.html', {'participants': top_participants})


def get_games_for_age(age):
    try:
        age = int(age)
    except (TypeError, ValueError):
        return []

    if 6 <= age <= 9:
        return Game.objects.filter(age_group='6-9')
    elif 10 <= age <= 13:
        return Game.objects.filter(age_group='10-13')
    elif 14 <= age <= 18:
        return Game.objects.filter(age_group='14-18')
    return []

@login_required
def participant_detail(request, uuid):
    participant = get_object_or_404(Participant, uuid=uuid)

    if request.method == 'POST':
        participant.name = request.POST.get('name')
        participant.age = request.POST.get('age')
        participant.points = request.POST.get('points')
        participant.save()
        return redirect('participant_detail', uuid=uuid)

    games = get_games_for_age(participant.age)

    return render(request, 'participant_detail.html', {
        'participant': participant,
        'games': games,
    })

