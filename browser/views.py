from django.http import HttpResponse
from django.shortcuts import render_to_response

import fspot.models as models

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
    tree = [{1:'States'}, [{2:'Kansas'}, [{40:'Lawrence'}, {41:'Tpoka'}], {21:'Illinois'}]]
    tree = _get_subtags(0)
    return render_to_response('tag_list.html', { 'tree': tree })

def tag(request, tag_id):
    photos = models.get_photos_with_tag(tag_id)
    name = models.get_tag_name(tag_id)
    return render_to_response('tag.html', {'name':name, 'photos':photos})
