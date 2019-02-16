from clippings import db
from clippings.models import Clip


def add_favorite(clip_id):
    clip = Clip.query.get(clip_id)
    if (clip.is_favorite):
        clip.is_favorite = False
    else: clip.is_favorite = True
    db.session.commit()

def add_like(clip_id, user):
    clip = Clip.query.get(clip_id)
    user.likes.append(clip)
    db.session.commit()

def remove_like(clip_id, user):
    clip = Clip.query.get(clip_id)
    user.likes.remove(clip)
    db.session.commit()
