from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    challenge = HiddenField('challenge', validators=[DataRequired()])
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    #remember_me = BooleanField('Recordar')
    submit = SubmitField('ACCEDER')
