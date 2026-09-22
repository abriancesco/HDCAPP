import os
from django.core.management.base import BaseCommand
from properties.models import Property, PropertyImage

class Command(BaseCommand):
    help = "Bulk import property photos from media/property_photos"

    def handle(self, *args, **kwargs):
        folder = "media/property_photos"

        for filename in os.listdir(folder):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            # Example: 21291_1.jpg → property_id = 21291
            property_id = filename.split("_")[0]

            try:
                prop = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"No property for {filename}"))
                continue

            PropertyImage.objects.create(
                property=prop,
                image=f"property_photos/{filename}"
            )

            self.stdout.write(self.style.SUCCESS(f"Imported {filename}"))
