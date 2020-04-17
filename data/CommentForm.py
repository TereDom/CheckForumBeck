from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    content = TextAreaField('Коментарий', validators=[DataRequired()])
    submit = SubmitField('Сохранить')