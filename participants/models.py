import uuid
from django.db import models

# Create your models here.
class Game(models.Model):
    AGE_GROUP_CHOICES = [
        ('6-9', '6-9'),
        ('10-13', '10-13'),
        ('14-18', '14-18'),
    ]
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)

    def __str__(self):
        return self.name

class Completion(models.Model):
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('participant', 'game')


class Participant(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    qr_image = models.ImageField(upload_to='barcodes/', blank=True)

    def __str__(self):
        return self.name or str(self.uuid)