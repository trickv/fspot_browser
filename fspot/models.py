import os
import datetime
import sqlite3
from django.db import models

def get_photos_with_month(month):
    next_month_year = month.year
    if month.month == 12:
        next_month_year += 1
        next_month_month = 1
    else:
        next_month_month = month.month + 1
    next_month = datetime.date(next_month_year, next_month_month, 1)
    photos = Photo.objects.filter(time__gte=month.strftime("%s"), time__lte=next_month.strftime("%s"))
    return photos

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

    def get_datetime(self):
        return datetime.datetime.fromtimestamp(self.time)

    def year_month(self):
        my_datetime = self.get_datetime()
        return datetime.datetime(my_datetime.year, my_datetime.month, 1)

    def remove_tag(self, tag):
        if not isinstance(tag, Tag):
            raise Exception("Must pass an instance of a tag (not a tag id)")
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("DELETE FROM photo_tags WHERE photo_id = %s AND tag_id = %s", [self.id, tag.id])
        transaction.commit_unless_managed()

    class Meta:
        db_table = u'photos'

