from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Participant, GameCompletion, Game


def index(request):
    top_participants = Participant.objects.order_by('-points')[:10]  # or other sorting field
    return render(request, 'index.html', {'participants': top_participants})

@login_required
def participant_detail(request, uuid):
    participant = get_object_or_404(Participant, uuid=uuid)

    # Determine age group
    age = participant.age
    if 6 <= age <= 9:
        group = '6-9'
    elif 10 <= age <= 13:
        group = '10-13'
    elif 14 <= age <= 18:
        group = '14-18'
    else:
        group = None

    # Show only games for their age group
    games = Game.objects.filter(age_group=group) if group else []

    if request.method == 'POST':
        # Handle name and age form
        participant.name = request.POST.get('name')
        participant.age = int(request.POST.get('age'))
        participant.save()

        # Update game completions
        for game in games:
            key = f'game_{game.id}'
            completed = request.POST.get(key) == 'on'
            obj, created = GameCompletion.objects.get_or_create(participant=participant, game=game)
            obj.completed = completed
            obj.save()

        return redirect('participant_detail', uuid=uuid)

    # Get current game completions
    completions = {
        gc.game.id: gc.completed for gc in GameCompletion.objects.filter(participant=participant)
    }

    # Calculate total points
    total_points = sum(
        gc.game.points for gc in GameCompletion.objects.filter(participant=participant, completed=True)
    )

    return render(request, 'participant_detail.html', {
        'participant': participant,
        'games': games,
        'completions': completions,
        'total_points': total_points,
    })
