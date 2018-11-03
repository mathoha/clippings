import os
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from clippings import db
from clippings.models import Clip, User
from clippings.clips.forms import UploadFileForm
from clippings.clips.parser import parse_file
from clippings.clips.utils import add_favorite



clips = Blueprint('clips', __name__)


@clips.route("/import", methods=['GET', 'POST'])
@login_required
def import_clips():
    form = UploadFileForm()
    if form.validate_on_submit():
        if form.clips_file.data:
            
            
            file_path = os.path.join('clippings/clips', 'temp.txt')
            form.clips_file.data.save(file_path)
            full_path = os.path.join(current_app.root_path, 'clips', 'temp.txt')
            print(full_path)
            count = parse_file(full_path, db, current_user)
            flash(f'{count} new clippings added!', 'success')
            return redirect(url_for('main.home'))


    return render_template('import.html.j2', title='Import', form=form)

order_by = {
    'page.asc()': Clip.page.asc(),
    'page.desc()': Clip.page.desc(),
    'date.asc()': Clip.date.asc(),
    'date.desc()': Clip.date.desc(),
    'author.asc()': Clip.author.asc(),
    'author.desc()': Clip.author.desc(),
    'title.asc()': Clip.author.asc(),
    'title.desc()': Clip.author.desc()
}


@clips.route("/<string:username>", methods=['GET', 'POST'])
@clips.route("/<string:username>/<string:title>", methods=['GET', 'POST'])
def user_book(username, title=None):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    clip_order = request.args.get('order_by', 'date.desc()')
    book_order = request.args.get('book_order', 'date.desc()')
    order = order_by.get(clip_order)
    b_order = order_by.get(book_order)
    clips_count = 0
    favorite_id = request.args.get('favorite_id')
    show_favorites = request.args.get('favorite')
    if(favorite_id):
        add_favorite(favorite_id)
    if(title == None):
        clips = Clip.query.filter_by(user_id=user.id).order_by(order).paginate(per_page=30, page=page)
        #seems inefficient to query again for count:
        clips_count = Clip.query.filter_by(user_id=user.id).count()
        favorite_count = Clip.query.filter_by(user_id=user.id, is_favorite=True).count()
        if(show_favorites):
            clips = Clip.query.filter_by(user_id=user.id, is_favorite=True).order_by(order).paginate(per_page=30, page=page)
    else:
        clip_order = request.args.get('order_by', 'page.asc()')
        order = order_by.get(clip_order) 
        clips = Clip.query.filter_by(user_id=user.id, title=title).order_by(order).paginate(per_page=30, page=page)
        clips_count = Clip.query.filter_by(user_id=user.id, title=title).count()
        favorite_count = Clip.query.filter_by(user_id=user.id, title=title, is_favorite=True).count()
        if(show_favorites):
            clips = Clip.query.filter_by(user_id=user.id, title=title, is_favorite=True).order_by(order).paginate(per_page=30, page=page)
    books = Clip.query.filter_by(user_id=user.id).order_by(b_order).group_by(Clip.title).distinct(Clip.title)
    books_count = Clip.query.filter_by(user_id=user.id).order_by(b_order).group_by(Clip.title).distinct(Clip.title).count()
    return render_template('user_book.html.j2', clips=clips, user=user, books=books, title_selected=title,
                           order_by=clip_order, book_order=book_order, clips_count=clips_count, books_count=books_count,
                           add_favorite=add_favorite, favorite_count=favorite_count, favorite=show_favorites)



@clips.route("/discover", methods=['GET', 'POST'])
def discover():
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.order_by(Clip.page.asc()).paginate(per_page=70, page=page)
    users = []
    for clip in clips.items:
        user = User.query.get(clip.user_id)
        users.append(user)
    clips_users_zip = zip(clips.items,users)
    clips_users = list(clips_users_zip)

    return render_template('discover.html.j2', clips_users=clips_users, clips=clips)


@clips.route("/discover1", methods=['GET', 'POST'])
def discover1():
    page = request.args.get('page', 1, type=int)
    clips = Clip.query.order_by(Clip.page.asc()).paginate(per_page=70, page=page)

    return render_template('discover.html.j2', clips=clips)


