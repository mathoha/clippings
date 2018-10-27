from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField


class UploadFileForm(FlaskForm):
    clips_file = FileField('Upload "My Clippings.txt" from your Kindle', validators=[FileAllowed(['txt'])])
    submit = SubmitField('Import')

    #could possible validate file before uploading
    #def validate_correct_format(self, clippings_file):
     
