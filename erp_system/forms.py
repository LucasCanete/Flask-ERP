from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(),Length(min=2,max=20)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recuerdame")
    submit = SubmitField("Entrar")


class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Contraseña",validators=[DataRequired()])
    confirm_password = PasswordField("Confirmar Contraseña", validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Crear Cuenta")


class ServiceForm(FlaskForm):
    type = StringField("Tipo de Servicio", validators=[DataRequired(),Length(min=2,max=20)])

    client_name = StringField("Cliente", validators=[DataRequired(),Length(min=2,max=20)])
    client_address = StringField("Direccion", validators=[Optional(),Length(min=2,max=50)])
    client_phone = StringField("Telefono", validators=[Optional(),Length(min=2,max=20)])

    comment = TextAreaField("Comentario", validators=[Optional(),Length(min=2,max=100)])
    submit = SubmitField("Guardar Servicio")
