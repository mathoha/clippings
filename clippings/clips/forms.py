from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField, BooleanField


class UploadFileForm(FlaskForm):
    clips_file = FileField('Upload "My Clippings.txt" from your Kindle', validators=[FileAllowed(['txt'])])
    only_new = BooleanField('Only New Clips')
    submit = SubmitField('Import')

    #could possible validate file before uploading
    #def validate_correct_format(self, clippings_file):

    #also check against the current content in database.
    #easiest to just compare date of latest and start from there. 
     
