from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Participant

def index(request):
    top_participants = Participant.objects.order_by('-points')[:10]  # or other sorting field
    return render(request, 'index.html', {'participants': top_participants})

@login_required
def participant_detail(request, uuid):
    participant = get_object_or_404(Participant, uuid=uuid)

    if request.method == 'POST':
        participant.name = request.POST.get('name')
        participant.age = request.POST.get('age')
        participant.points = request.POST.get('points')
        participant.save()
        return redirect('participant_detail', uuid=uuid)

    return render(request, 'participant_detail.html', {'participant': participant})
