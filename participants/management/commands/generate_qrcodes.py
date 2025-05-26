import os
import qrcode
from django.core.management.base import BaseCommand
from participants.models import Participant
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate 5000 unique QR codes for participants'

    def handle(self, *args, **kwargs):
        base_url = "https://balafest.onrender.com/participant/"
        output_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(output_dir, exist_ok=True)

        for i in range(5000):
            participant = Participant.objects.create()
            qr_data = f"{base_url}{participant.uuid}"

            img = qrcode.make(qr_data)

            filename = os.path.join(output_dir, f"{participant.uuid}.png")
            img.save(filename)

            participant.qr_image = f"qrs/{participant.uuid}.png"
            participant.save()

        self.stdout.write(self.style.SUCCESS("Successfully generated 5000 QR codes"))