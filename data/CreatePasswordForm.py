from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class ForgetForm(FlaskForm):
    code = StringField('Введите код подтверждения', validators=[DataRequired()])
    submit = SubmitField('Отправить')