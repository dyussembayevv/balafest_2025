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
    first_place_points = models.PositiveIntegerField(default=10)
    second_place_points = models.PositiveIntegerField(default=7)
    third_place_points = models.PositiveIntegerField(default=5)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    is_ranked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class GameCompletion(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    PLACE_CHOICES = [
        (1, '1st Place'),
        (2, '2nd Place'),
        (3, '3rd Place'),
    ]
    place = models.PositiveSmallIntegerField(choices=PLACE_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ('participant', 'game')

    def get_awarded_points(self):
        if self.place == 1:
            return self.game.first_place_points
        elif self.place == 2:
            return self.game.second_place_points
        elif self.place == 3:
            return self.game.third_place_points
        return 0


class GamePlacement(models.Model):
    PLACE_CHOICES = [
        (1, '1st Place'),
        (2, '2nd Place'),
        (3, '3rd Place'),
    ]

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='placements')
    place = models.IntegerField(choices=PLACE_CHOICES)
    points_awarded = models.PositiveIntegerField()

    class Meta:
        unique_together = ('participant', 'game')

    def __str__(self):
        return f"{self.participant.name} - {self.game.name} - {self.get_place_display()}"
