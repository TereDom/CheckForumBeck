from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class CodeForm(FlaskForm):
    code = StringField('* Введите код подтверждения', validators=[DataRequired()])
    password = PasswordField('* Пароль', validators=[DataRequired()])
    password_again = PasswordField('* Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Принять')