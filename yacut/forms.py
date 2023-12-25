from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import Length, Optional


class Link_Form(FlaskForm):
    original_link = URLField([Optional()])
    custom_id = StringField(validators=[Length(1, 16), Optional()])
    submit = SubmitField('Создать')
