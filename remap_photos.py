import os
import re
from django.core.files import File
from properties.models import Property, PropertyImage

PHOTO_DIR = os.path.join("media", "property_photos")

def run():
    folder = os.path.join(os.getcwd(), PHOTO_DIR)

    if not os.path.isdir(folder):
        print(f"Folder not found: {folder}")
        return

    count = 0

    for filename in os.listdir(folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Extract ID from filename: 21291_1.jpg → 21291
        match = re.match(r"(\d+)", filename)
        if not match:
            print(f"Skipping unrecognized filename: {filename}")
            continue

        access_id = int(match.group(1))

        try:
            prop = Property.objects.get(access_id=access_id)
        except Property.DoesNotExist:
            print(f"No property for photo: {filename}")
            continue

        filepath = os.path.join(folder, filename)

        with open(filepath, "rb") as f:
            img = PropertyImage(property=prop)
            img.image.save(filename, File(f), save=True)

        count += 1

    print(f"Photo remapping complete. {count} photos attached.")
