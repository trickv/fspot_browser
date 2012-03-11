import Image
import tempfile
import os

from django.http import HttpResponse

import fspot.models as models

def raw(request, photo_id):
    filename = models.get_photo_filename(photo_id)
    image = Image.open(filename)
    # TODO: determine mime type
    mime_type = 'image/jpeg'
    image_file = open(filename)
    data = image_file.read()
    image_file.close()
    return HttpResponse(data, mimetype=mime_type)

def thumbnail(request, photo_id):
    filename = models.get_photo_filename(photo_id)
    image = Image.open(filename)

    short_side = 132

    width, height = image.size
    if width < height:
        thumb_size = (short_side, short_side * 4 / 3)
    else:
        thumb_size = (short_side * 4 / 3, short_side)
    image.thumbnail(thumb_size, Image.ANTIALIAS)

    temp_file = tempfile.TemporaryFile()
    image.save(temp_file, "jpeg")
    temp_file.seek(0)
    data = temp_file.read()
    temp_file.close()

    return HttpResponse(data, mimetype='image/jpeg')
