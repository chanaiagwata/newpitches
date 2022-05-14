from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired


class Pitch_form(FlaskForm):
    Pitch_form = TextAreaField('Enter new pitch')
    submit = SubmitField('Submit')
    
class Category_form(FlaskForm):
    name = StringField('Pitch category', validators=[DataRequired()])
    submit = SubmitField('Add to Category')
    
class Comment_form(FlaskForm):
    remark = TextAreaField('Add a comment')
    submit = SubmitField('Submit')
