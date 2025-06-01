import uuid
from django.db import models

# Create your models here.
AGE_GROUP_CHOICES = [
    ('6-9', '6-9'),
    ('10-13', '10-13'),
    ('14-18', '14-18'),
]

class Game(models.Model):
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=10)  # Примеры: '6-9', '10-13', '14-18'

    def __str__(self):
        return f"{self.name} ({self.age_group})"


class Participant(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    qr_image = models.ImageField(upload_to='barcodes/', blank=True)

    def __str__(self):
        return self.name or str(self.uuid)