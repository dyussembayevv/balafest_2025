from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('participant/<uuid:uuid>/', views.participant_detail, name='participant_detail'),
]
