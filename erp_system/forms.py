from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
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

class SaleForm(FlaskForm):
    customer = SelectField("Cliente", choices = ["Consumidor","Instalador"], validators=[DataRequired(),Length(min=2,max=20)])
    product = StringField("Producto", validators=[DataRequired(),Length(min=2,max=30)])
    qty = IntegerField(validators=[DataRequired()])
    price_paid = IntegerField(validators=[DataRequired()])
    payment_method = SelectField("Metodo de Pago", choices = ["Efectivo","Transferencia", "Tarjeta","Pagare"], validators=[DataRequired(),Length(min=2,max=10)])

    submit = SubmitField("Crear Venta")

class ServiceForm(FlaskForm):
    type = StringField("Tipo de Servicio", validators=[DataRequired(),Length(min=2,max=20)])

    client_name = StringField("Cliente", validators=[DataRequired(),Length(min=2,max=20)])
    client_address = StringField("Direccion", validators=[Optional(),Length(min=2,max=50)])
    client_phone = StringField("Telefono", validators=[Optional(),Length(min=2,max=20)])

    comment = TextAreaField("Comentario", validators=[Optional(),Length(min=2,max=100)])
    submit = SubmitField("Guardar Servicio")


class DownloadForm(FlaskForm):
    chosen_date = StringField("Cliente", validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField("Mostrar Reporte")
