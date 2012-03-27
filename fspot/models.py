import os
import datetime
import sqlite3
from django.db import models

##### DEPRECATED
# These functions should be replaced with querying the models themselves.
db = sqlite3.connect('db/photos.db')

def get_tags_with_parent(parent_tag_id):
    c = db.cursor()
    c.execute("SELECT id, name FROM tags WHERE category_id = ? ORDER BY name", (parent_tag_id,))
    tags = []
    for row in c:
        tags.append({row[0]:row[1]})
    return tags

def get_photos_with_month(month):
    next_month_year = month.year
    if month.month == 12:
        next_month_year += 1
        next_month_month = 1
    else:
        next_month_month = month.month + 1
    next_month = datetime.date(next_month_year, next_month_month, 1)
    c = db.cursor()
    c.execute("SELECT * FROM photos WHERE time BETWEEN ? AND ? ORDER BY time ASC", (month.strftime("%s"), next_month.strftime("%s")))
    photos = []
    for row in c:
        photos.append({row[0]:row[4]})
    return photos

def get_earliest_time():
    c = db.cursor()
    c.execute("SELECT MIN(time) FROM photos")
    row = c.fetchone()
    return datetime.datetime.fromtimestamp(row[0])

def get_newest_time():
    c = db.cursor()
    c.execute("SELECT MAX(time) FROM photos")
    row = c.fetchone()
    return datetime.datetime.fromtimestamp(row[0])

####### END OF DEPRECATED FUNCTIONS

class Export(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.IntegerField()
    image_version_id = models.IntegerField()
    export_type = models.TextField()
    export_token = models.TextField()

    class Meta:
        db_table = u'exports'

class Jobs(models.Model):
    id = models.IntegerField(primary_key=True)
    job_type = models.TextField()
    job_options = models.TextField()
    run_at = models.IntegerField(null=True, blank=True)
    job_priority = models.IntegerField()

    class Meta:
        db_table = u'jobs'

class Meta(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    data = models.TextField(blank=True)

    class Meta:
        db_table = u'meta'

class PhotoVersion(models.Model):
    """
    Django 1.3 does not support primary keys across multiple fields.
    Thus, we can't properly relate this to the Photo model as the table
    exists from F-Spot.
    """
    photo_id = models.IntegerField()
    version_id = models.IntegerField()
    name = models.TextField(blank=True)
    base_uri = models.TextField()
    filename = models.TextField()
    import_md5 = models.TextField(blank=True)
    protected = models.BooleanField()

    class Meta:
        db_table = u'photo_versions'

class Roll(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.IntegerField()

    class Meta:
        db_table = u'rolls'

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    is_category = models.BooleanField()
    sort_priority = models.IntegerField(null=True, blank=True)
    icon = models.TextField(blank=True)

    def __repr__(self):
        return "<Tag %d:%s>" % (self.id, self.name)

    class Meta:
        db_table = u'tags'

class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    base_uri = models.TextField()
    filename = models.TextField()
    description = models.TextField()
    roll = models.ForeignKey(Roll)
    default_version_id = models.IntegerField()
    rating = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, db_table='photo_tags')

    def file_path(self):
        file_path = self.base_uri.replace('file://', '')
        if file_path[-1] != os.sep:
            file_path += os.sep
        file_path += self.filename
        return file_path

    def __repr__(self):
        return "<Photo %d:%s>" % (self.id, self.filename)

    class Meta:
        db_table = u'photos'

