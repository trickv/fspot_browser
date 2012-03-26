import datetime
import sqlite3
from django.db import models

db = sqlite3.connect('db/photos.db')

def get_photo_filename(photo_id):
    c = db.cursor()
    c.execute("SELECT * FROM photos WHERE id = ?", (photo_id,))
    row = c.fetchone()
    uri = row[2] + '/' + row[3] # FIXME: conditionally do this
    filename = uri.replace("file://", "")
    return filename

def get_tags_with_parent(parent_tag_id):
    c = db.cursor()
    c.execute("SELECT id, name FROM tags WHERE category_id = ? ORDER BY name", (parent_tag_id,))
    tags = []
    for row in c:
        tags.append({row[0]:row[1]})
    return tags

def get_tag_name(tag_id):
    c = db.cursor()
    c.execute("SELECT name FROM tags WHERE id = ?", (tag_id,))
    row = c.fetchone()
    return row[0]

def get_photos_with_tag(tag_id):
    c = db.cursor()
    c.execute("SELECT * FROM photos JOIN photo_tags ON (photos.id = photo_tags.photo_id) WHERE tag_id = ? ORDER BY time ASC", (tag_id,))
    photos = []
    for row in c:
        photos.append({row[0]:row[4]})
    return photos

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

def get_photo_object(photo_id):
    c = db.cursor()
    c.execute("SELECT * FROM photos WHERE id = ?", (photo_id,))
    row = c.fetchone()
    return {'id':photo_id, 'filename':get_photo_filename(photo_id), 'description':row[4]}

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
