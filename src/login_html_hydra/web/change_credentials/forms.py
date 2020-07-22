from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ChangeCredentialsForm(FlaskForm):
    password = PasswordField('Clave Actual', validators=[DataRequired()])
    password2 = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    password2_confirmation = PasswordField('Repetir Contraseña', validators=[DataRequired()])
    submit = SubmitField('CONTINUAR')