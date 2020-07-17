from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Clave', validators=[DataRequired()])
    #remember_me = BooleanField('Recordar')
    submit = SubmitField('Aceptar')