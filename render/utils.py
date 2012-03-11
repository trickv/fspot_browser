import ExifTags
import Image

def get_exif(filename):
    try:
        image = Image.open(filename)
    except IOError:
        return {}
    return _get_exif_for_image(image)

def _get_exif_for_image(image):
    ret = {}
    info = image._getexif()
    for tag, value in info.items():
        decoded = ExifTags.TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
