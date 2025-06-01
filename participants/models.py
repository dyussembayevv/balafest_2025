import uuid
from django.db import models

# Create your models here.
class Participant(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    qr_image = models.ImageField(upload_to='barcodes/', blank=True)

    def __str__(self):
        return self.name or str(self.uuid)