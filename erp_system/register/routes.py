from flask import Blueprint,render_template, redirect,flash, url_for
from erp_system.forms import RegisterForm
from flask_login import current_user
from erp_system import db, bcrypt
from erp_system.models import User

register_bp = Blueprint('register_bp',__name__)

@register_bp.route("/register", methods=["GET","POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home_page'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Cuenta ha sido creada para {form.username.data}! Ahora puede iniciar sesion','success')
        return redirect(url_for('login_bp.login_page'))
    return render_template("register.html", title= "Inscribirse", form=form)
