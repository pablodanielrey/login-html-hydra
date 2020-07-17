from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class InputCode(FlaskForm):
    code = StringField('Código', validators=[DataRequired()])
    submit = SubmitField('Aceptar')


class InputCredentials(FlaskForm):
    password = PasswordField('Clave', validators=[DataRequired()])
    password2 = PasswordField('Reconfirmar clave', validators=[DataRequired()])
    submit = SubmitField('Aceptar')

class InputUsername(FlaskForm):
    username = StringField('DNI', validators=[DataRequired()])
    submit = SubmitField('Aceptar')
