import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Max, Min

import fspot.models as models
import render.utils

def _get_subtags(tag_id):
    tags = models.Tag.objects.filter(category_id=tag_id).order_by('name')
    tree = []
    for tag in tags:
        tree.append(tag)
        subtags = _get_subtags(tag.id)
        if len(subtags) > 0:
            tree.append(subtags)
    return tree

def tag_list(request):
    tree = _get_subtags(0)
    return render_to_response('tag_list.html', { 'tree': tree })

def tag(request, tag_id):
    tag = models.Tag.objects.get(id=tag_id)
    photos = tag.photo_set.all().order_by('time')
    return render_to_response('photo_list.html', {'name':tag.name, 'photos':photos})

def hack_remove_best(request, photo_id):
    p = models.Photo.objects.get(id=photo_id)
    t = models.Tag.objects.get(id=253)
    p.remove_tag(t)
    return HttpResponseRedirect('/photo/%s/' % photo_id)

def hack_remove_tag(request, photo_id, tag_id):
    p = models.Photo.objects.get(id=photo_id)
    t = models.Tag.objects.get(id=tag_id)
    p.remove_tag(t)
    return HttpResponseRedirect('/photo/%s/' % photo_id)

def hack_best_2011(request, photo_id):
    p = models.Photo.objects.get(id=photo_id)
    t = models.Tag.objects.get(id=253)
    p.tags.add(t)
    p.save()
    return HttpResponseRedirect('/photo/%s/' % photo_id)

def hack_add_tag(request, photo_id, tag_id):
    p = models.Photo.objects.get(id=photo_id)
    t = models.Tag.objects.get(id=tag_id)
    p.tags.add(t)
    p.save()
    return HttpResponseRedirect('/photo/%s/' % photo_id)

def month(request, year_int, month_int):
    year_int = int(year_int)
    month_int = int(month_int)
    month = datetime.date(year_int, month_int, 1)
    photos = models.get_photos_with_month(month)
    name = "%d-%d" % (year_int, month_int)
    return render_to_response('photo_list.html', {'name':name, 'photos':photos})

def photo(request, photo_id):
    photo = models.Photo.objects.get(id=photo_id)
    exif = render.utils.get_exif(photo.file_path())
    if exif.has_key('MakerNote'):
        exif.pop('MakerNote')
    photo.exif = exif
    return render_to_response('photo.html', {'photo':photo})

def _yearmonth_list():
    start = datetime.datetime.fromtimestamp(models.Photo.objects.all().aggregate(Min('time'))['time__min'])
    end = datetime.datetime.fromtimestamp(models.Photo.objects.all().aggregate(Max('time'))['time__max'])
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
