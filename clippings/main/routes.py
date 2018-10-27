from flask import Blueprint
from flask import render_template, request, Blueprint
from flask_login import current_user
from clippings.models import Post,Clip, User
from clippings import db


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    db.create_all() #this bootstraps the database within the same thread, a workaround for the test version
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.order_by(Clip.date.desc()).paginate(per_page=7, page=page)
    users = []
    for clip in clips.items:
        user = User.query.get(clip.user_id)
        users.append(user)
    clips_users_zip = zip(clips.items,users)
    clips_users = list(clips_users_zip)

    return render_template('home.html.j2', clips_users=clips_users, clips=clips)

@main.route("/about")
def about():
    return render_template('about.html.j2', title='About')



