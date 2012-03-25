from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter()
def tag_tree(value, autoescape=None):
    """
    Portions of this function are taken from django/template/defaultfilters.py
    Based on the django stock filter unordered_list but hacked to work for key+value pairs.

    Items are assumed to be dictionaries.  So it looks like:
    [{10:'A tag'}, [{100:'A subtag'}, {200:'Another subtag'}], {20:'Another tag'}]
    """
    if autoescape:
        from django.utils.html import conditional_escape
        escaper = conditional_escape
    else:
        escaper = lambda x: x
    def _helper(list_, tabs=1):
        indent = u'\t' * tabs
        output = []

        list_length = len(list_)
        i = 0
        while i < list_length:
            title = list_[i]
            sublist = ''
            sublist_item = None
            if isinstance(title, (list, tuple)):
                sublist_item = title
                title = ''
            elif i < list_length - 1:
                next_item = list_[i+1]
                if next_item and isinstance(next_item, (list, tuple)):
                    # The next item is a sub-list.
                    sublist_item = next_item
                    # We've processed the next item now too.
                    i += 1
            if sublist_item:
                sublist = _helper(sublist_item, tabs+1)
                sublist = '\n%s<ul>\n%s\n%s</ul>\n%s' % (indent, sublist,
                                                         indent, indent)
            tag_id = title.keys()[0]
            tag_name = title[tag_id]
            output.append("%s<li><a href='/tag/%d/'>%s</a>%s</li>" %
                (indent, tag_id, tag_name, sublist))
            i += 1
        return '\n'.join(output)
    return mark_safe(_helper(value))
tag_tree.is_safe = True
tag_tree.needs_autoescape = True

