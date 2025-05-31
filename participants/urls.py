from django.urls import path
from . import views

urlpatterns = [
    path('participant/<uuid:uuid>/', views.participant_detail, name='participant_detail'),
]
