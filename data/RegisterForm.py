from flask_wtf import FlaskForm
from wtforms import PasswordField, TextAreaField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('* Почта', validators=[DataRequired()])
    password = PasswordField('* Пароль', validators=[DataRequired()])
    password_again = PasswordField('* Повторите пароль', validators=[DataRequired()])
    name = StringField('* Имя пользователя', validators=[DataRequired()])
    vk_id = StringField('ID ВКонтакте')
    submit = SubmitField('Войти')
