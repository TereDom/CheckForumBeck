from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewWikiPostForm(FlaskForm):
    title = StringField('Заголовок поста', validators=[DataRequired()])
    status = StringField('Тип объекта', validators=[DataRequired()])
    image = FileField('Загрузить изображение')
    content = TextAreaField('Добавить содержание', validators=[DataRequired()])
    submit = SubmitField('Добавить пост')
