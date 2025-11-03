from flask import Blueprint, render_template, flash, url_for, redirect, request
from erp_system.models import User
from erp_system.forms import LoginForm
from flask_login import current_user, login_user
from erp_system import bcrypt

login_bp = Blueprint('login_bp',__name__)

@login_bp.route("/login", methods=["GET","POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('service_bp.services_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("service_bp.services_page"))
        else:
            flash('Inicio de sesion incorrecto. Revisa el Usuario y Contraseña', 'danger')

    return render_template("login.html", title="Iniciar sesion", form=form)
