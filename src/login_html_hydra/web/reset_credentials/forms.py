from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class InputCode(FlaskForm):
    cid = HiddenField('cid', validators=[DataRequired()])
    code = StringField('Código', validators=[DataRequired()])
    submit = SubmitField('CONTINUAR')


class InputCredentials(FlaskForm):
    cid = HiddenField('cid', validators=[DataRequired()])
    password = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired()])
    submit = SubmitField('CONTINUAR')

class InputUsername(FlaskForm):
    username = StringField('Ingrese su DNI', validators=[DataRequired()])
    submit = SubmitField('CONTINUAR')
