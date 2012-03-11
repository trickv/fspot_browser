import sqlite3
from django.db import models

def get_photo_filename(photo_id):
    db = sqlite3.connect('db/photos.db')
    c = db.cursor()
    c.execute("SELECT * FROM photos WHERE id = ?", (photo_id,))
    row = c.fetchone()
    uri = row[2] + '/' + row[3] # FIXME: conditionally do this
    filename = uri.replace("file://", "")
    return filename
