import uuid
from django.db import models

# Create your models here.
class Participant(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)
    # points = models.IntegerField(default=0) ← optional or delete

    def __str__(self):
        return self.name or str(self.uuid)

class Game(models.Model):
    AGE_GROUP_CHOICES = [
        ('6-9', '6-9'),
        ('10-13', '10-13'),
        ('14-18', '14-18'),
    ]

    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.points} pts)"

class GameCompletion(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('participant', 'game')
