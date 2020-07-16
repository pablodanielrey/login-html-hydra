from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ChangeCredentialsForm(FlaskForm):
    password = PasswordField('Clave Actual', validators=[DataRequired()])
    password2 = PasswordField('Clave Nueva', validators=[DataRequired()])
    password2_confirmation = PasswordField('Confirmar Clave Nueva', validators=[DataRequired()])
    submit = SubmitField('Aceptar')