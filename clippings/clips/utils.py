from clippings import db
from clippings.models import Clip


def add_favorite(clip_id):
    clip = Clip.query.get(clip_id)
    if (clip.is_favorite):
        clip.is_favorite = False
    else: clip.is_favorite = True
    db.session.commit()