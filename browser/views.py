import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response

import fspot.models as models
import render.utils

def _get_subtags(tag_id):
    tags = models.get_tags_with_parent(tag_id)
    tree = []
    for tag in tags:
        tree.append(tag)
        subtags = _get_subtags(tag.keys()[0])
        if len(subtags) > 0:
            tree.append(subtags)
    return tree

def tag_list(request):
    tree = _get_subtags(0)
    return render_to_response('tag_list.html', { 'tree': tree })

def tag(request, tag_id):
    photos = models.get_photos_with_tag(tag_id)
    name = models.get_tag_name(tag_id)
    return render_to_response('photo_list.html', {'name':name, 'photos':photos})

def month(request, year_int, month_int):
    year_int = int(year_int)
    month_int = int(month_int)
    month = datetime.date(year_int, month_int, 1)
    photos = models.get_photos_with_month(month)
    name = "%d-%d" % (year_int, month_int)
    return render_to_response('photo_list.html', {'name':name, 'photos':photos})

def photo(request, photo_id):
    photo = models.get_photo_object(photo_id)
    exif = render.utils.get_exif(photo['filename'])
    if exif.has_key('MakerNote'):
        exif.pop('MakerNote')
    photo['exif'] = exif
    return render_to_response('photo.html', {'photo':photo})

def _yearmonth_list():
    start = models.get_earliest_time()
    end = models.get_newest_time()
    year = start.year
    month = start.month
    list = []
    while True:
        month_datetime = datetime.datetime(year, month, 1)
        photo_count = len(models.get_photos_with_month(month_datetime))
        if photo_count > 0:
            list.append((month_datetime, photo_count, ))
        month += 1
        if month > 12:
            month = 1
            year += 1
        if year > end.year or (year >= end.year and month > end.month):
            break
    return list

def time(request):
    month_list = _yearmonth_list()
    return render_to_response('time.html', {'months':month_list})
