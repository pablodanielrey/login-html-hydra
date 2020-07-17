from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Clave', validators=[DataRequired()])
    challenge = HiddenField('challenge', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
