import Image
import tempfile
import os

from django.http import HttpResponse

import fspot.models as models
import utils

def raw(request, photo_id):
    # FIXME: this function should detect rotation and compensate!
    photo = models.Photo.objects.get(id=photo_id)
    image = Image.open(photo.file_path())
    # TODO: determine mime type
    mime_type = 'image/jpeg'
    image_file = open(photo.file_path())
    data = image_file.read()
    image_file.close()
    return HttpResponse(data, mimetype=mime_type)

def thumbnail(request, photo_id):
    photo = models.Photo.objects.get(id=photo_id)
    image = Image.open(photo.file_path())

    short_side = 132

    width, height = image.size
    if width < height:
        thumb_size = (short_side, short_side * 4 / 3)
    else:
        thumb_size = (short_side * 4 / 3, short_side)
    image.thumbnail(thumb_size, Image.ANTIALIAS)
    image = _rotate_to_exif(image)

    temp_file = tempfile.TemporaryFile()
    image.save(temp_file, "jpeg")
    temp_file.seek(0)
    data = temp_file.read()
    temp_file.close()

    return HttpResponse(data, mimetype='image/jpeg')

def scale(request, photo_id, request_width):
    photo = models.Photo.objects.get(id=photo_id)
    image = Image.open(photo.file_path())

    width, height = image.size
    aspect = float(width) / float(height)
    new_height = int(float(request_width) * aspect)
    image.thumbnail((int(request_width), new_height), Image.ANTIALIAS)
    image = _rotate_to_exif(image)

    temp_file = tempfile.TemporaryFile()
    image.save(temp_file, "jpeg")
    temp_file.seek(0)
    data = temp_file.read()
    temp_file.close()

    return HttpResponse(data, mimetype='image/jpeg')

def _rotate_to_exif(image):    
    exif = utils._get_exif_for_image(image)
    if not exif.has_key('Orientation'):
        return image
    orientation = exif['Orientation']
    if orientation == 6:
        image = image.rotate(270)
    elif orientation == 8:
        image = image.rotate(90)
    elif orientation == 3:
        image = image.rotate(180)
    return image
