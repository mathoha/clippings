import os
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from clippings import db
from clippings.models import Clip, User
from clippings.clips.forms import UploadFileForm
from clippings.clips.parser import parse_file
from werkzeug.utils import secure_filename

clips = Blueprint('clips', __name__)


@clips.route("/import", methods=['GET', 'POST'])
@login_required
def import_clips():
    form = UploadFileForm()
    if form.validate_on_submit():
        if form.clips_file.data:
            flash('10 new clippings added!', 'success')
            
            file_path = os.path.join('clippings/clips', 'temp.txt')
            form.clips_file.data.save(file_path)
            full_path = os.path.join(current_app.root_path, 'clips', 'temp.txt')
            print(full_path)
            parse_file(full_path, db, current_user)
            return redirect(url_for('main.home'))


    return render_template('import.html.j2', title='Import', form=form)


@clips.route("/<string:username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.filter_by(user_id=user.id).order_by(Clip.date.desc()).paginate(per_page=30, page=page)
    books = Clip.query.filter_by(user_id=user.id).order_by(Clip.date.desc()).group_by(Clip.title).distinct(Clip.title)
    clips1 = clips.items[0:(len(clips.items)//2):1]
    clips2 = clips.items[(len(clips.items)//2)::1]
    return render_template('user_book.html.j2', clips=clips, clips1=clips1 , clips2=clips2, user=user, books=books)



@clips.route("/<string:username>/<string:title>")
def user_book(username, title):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.filter_by(user_id=user.id, title=title).order_by(Clip.page.asc()).paginate(per_page=30, page=page)
    clips1 = clips.items[0:(len(clips.items)//2):1]
    clips2 = clips.items[(len(clips.items)//2)::1]
    books = Clip.query.filter_by(user_id=user.id).order_by(Clip.date.desc()).group_by(Clip.title).distinct(Clip.title)
    return render_template('user_book.html.j2', clips=clips, clips1=clips1 , clips2=clips2, user=user, books=books, title_selected=title)



@clips.route("/discover", methods=['GET', 'POST'])
def discover():
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.order_by(Clip.date.desc()).paginate(per_page=70, page=page)
    users = []
    for clip in clips.items:
        user = User.query.get(clip.user_id)
        users.append(user)
    clips_users_zip = zip(clips.items,users)
    clips_users = list(clips_users_zip)

    return render_template('discover.html.j2', clips_users=clips_users, clips=clips)