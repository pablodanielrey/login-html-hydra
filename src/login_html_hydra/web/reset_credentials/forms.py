from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class InputCode(FlaskForm):
    code = StringField('Código', validators=[DataRequired()])

class InputCredentials(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired()])

class InputUsername(FlaskForm):
    username = StringField('Ingrese su DNI', validators=[DataRequired()])
