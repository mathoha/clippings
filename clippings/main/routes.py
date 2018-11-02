from flask import Blueprint
from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from clippings.models import Post, Clip, User
from clippings import db


main = Blueprint('main', __name__)

@main.route("/home")
@login_required
def home():
    
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.filter_by(user_id=current_user.id).order_by(Clip.date.desc()).paginate(per_page=7, page=page)
    books = Clip.query.filter_by(user_id=current_user.id).order_by(Clip.date.desc()).group_by(Clip.title).distinct(Clip.title)
    return render_template('home.html.j2', user=current_user, clips=clips, books=books)


@main.route("/about")
def about():
    return render_template('about.html.j2', title='About')


@main.route("/")
@main.route("/landing")
def landing():
    db.create_all() #this bootstraps the database within the same thread, a workaround for the test version
    return render_template('about.html.j2')