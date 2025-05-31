from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Participant, GameCompletion, Game
from django.db.models import Sum, Q



def index(request):
    top_participants = Participant.objects.annotate(
        total_points=Sum('gamecompletion__game__points', filter=Q(gamecompletion__completed=True))
    ).order_by('-total_points')[:10]

    return render(request, 'index.html', {'participants': top_participants})

@login_required
def participant_detail(request, uuid):
    participant = get_object_or_404(Participant, uuid=uuid)

    # Determine age group of participant
    age = participant.age
    if 6 <= age <= 9:
        age_group = '6-9'
    elif 10 <= age <= 13:
        age_group = '10-13'
    elif 14 <= age <= 18:
        age_group = '14-18'
    else:
        age_group = None  # or handle out of range

    # Get games for participant's age group
    games = Game.objects.filter(age_group=age_group) if age_group else Game.objects.none()

    # Get existing completions for participant (dict game.id -> completion obj)
    completions = {gc.game_id: gc for gc in GameCompletion.objects.filter(participant=participant)}

    if request.method == 'POST':
        # Update participant info
        participant.name = request.POST.get('name')
        participant.age = int(request.POST.get('age'))
        participant.save()

        # Update game completions
        for game in games:
            completed = request.POST.get(f'game_{game.id}') == 'on'
            if game.id in completions:
                # update existing
                gc = completions[game.id]
                gc.completed = completed
                gc.save()
            else:
                # create new completion record if completed
                if completed:
                    GameCompletion.objects.create(participant=participant, game=game, completed=True)

        # Redirect to refresh page and recalc age group if changed
        return redirect('participant_detail', uuid=uuid)

    # Calculate total points (sum of completed games points)
    total_points = sum(game.points for game in games if completions.get(game.id, None) and completions[game.id].completed)

    return render(request, 'participant_detail.html', {
        'participant': participant,
        'games': games,
        'completions': completions,
        'total_points': total_points
    })
