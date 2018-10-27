import os
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from clippings import db
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