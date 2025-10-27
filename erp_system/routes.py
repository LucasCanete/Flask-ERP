from flask import render_template, flash, redirect, url_for, request, jsonify
from erp_system import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from erp_system.forms import (LoginForm, RegisterForm, ServiceForm)
from erp_system.models import User, Service
from datetime import datetime, timedelta
from sqlalchemy import func
from collections import defaultdict
'''
When First running to create db execute



from erp_system import db, app
app.app_context().push()
db.create_all()

This will create db inside instances
'''

"""

@app.route("/")
@login_required
def home_page():
    status_filter = request.args.get("status")
    date_filter = request.args.get("date")

    services = Service.query

    if status_filter:
        services = services.filter_by(status=status_filter)

    services = services.order_by(Service.datetime.desc()).all()

    #group by day
    grouped = defaultdict(list)
    for service in services:
        day_str = service.datetime.strftime("%d/%m/%Y")
        grouped[day_str].append(service)

    # Convertir a lista de tuplas ordenada por fecha (reciente primero)
    grouped_services = sorted(grouped.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=True)

    return render_template("home.html", title="Servicios", grouped_services=grouped_services)


#update status in real time from the home page via drop down menu
@app.route("/update_status/<int:service_id>", methods=['POST'])
@login_required
def update_status(service_id):
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['En proceso', 'Completado', 'Cancelado']:
        return jsonify({'error': 'Estado inválido'}), 400

    service = Service.query.get_or_404(service_id)
    service.status = new_status
    db.session.commit()

    return jsonify({'success': True, 'new_status': new_status}), 200



@app.route("/logout")
def logout():
    logout_user()
    return(redirect(url_for('login_page')))



@app.route("/login", methods=["GET","POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home_page"))
        else:
            flash('Inicio de sesion incorreco. Revisa el Usuario y Contraseña', 'danger')

    return render_template("login.html", title="Iniciar sesion", form=form)
"""
"""
@app.route("/register", methods=["GET","POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Cuenta ha sido creada para {form.username.data}! Ahora puede iniciar sesion','success')
        return redirect(url_for('login_page'))
    return render_template("register.html", title= "Inscribirse", form=form)


@app.route("/service", methods=["GET","POST"])
@login_required
def service_page():
    form = ServiceForm()
    if form.validate_on_submit():
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        service = Service( type=form.type.data, client_name = form.client_name.data, client_address=form.client_address.data, client_phone=form.client_phone.data, status='En proceso', comment=form.comment.data)
        db.session.add(service)
        db.session.commit()
        flash(f'Nuevo servicio ha sido creado!','success')
        return redirect(url_for('home_page'))
    return render_template("service.html", title="Servicio", form=form)

@app.route("/edit_service/<id>", methods=['GET', 'POST'])
@login_required
def edit_service_page(id):
    form = ServiceForm()

    service = Service.query.filter_by(id=id).first()
    if not service:
        flash("Servicio no encontrado.", "danger")
        return redirect(url_for("home_page"))

    #Prefill the form with the values from the service
    if request.method == 'GET':
        form.type.data = service.type

        form.client_name.data = service.client_name
        form.client_address.data = service.client_address
        form.client_phone.data = service.client_phone
        form.comment.data = service.comment

    if form.validate_on_submit():
        service.type = form.type.data
        service.client_name = form.client_name.data
        service.client_address = form.client_address.data
        service.client_phone = form.client_phone.data
        service.comment = form.comment.data
        db.session.commit()
        flash(f'Servicio ha sido editado!','success')
        return redirect(url_for("home_page"))

    return render_template("edit_service.html", title="Editar Servicio", form=form, service=service )


@app.route("/delete_service/<id>", methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.filter_by(id=id).first()
    if service:
        db.session.delete(service)
        db.session.commit()
        flash('Servicio eliminado correctamente.', 'success')
    else:
        flash('Servicio no encontrado.', 'danger')
    return redirect(url_for("home_page"))


@app.route('/history')
@login_required
def history_page():
    return render_template('history.html')

@app.route('/api/history_data')
@login_required
def historial_data():
    periodo = request.args.get('periodo', 'semana')
    hoy = datetime.now()

    if periodo == 'semana':
        desde = hoy - timedelta(days=7)
        agrupado_por = func.strftime('%d/%m', Service.datetime)  # Día/Mes
    elif periodo == 'mes':
        desde = hoy - timedelta(days=30)
        agrupado_por = func.strftime('%d/%m', Service.datetime)
    elif periodo == 'anio':
        desde = hoy - timedelta(days=365)
        agrupado_por = func.strftime('%m/%Y', Service.datetime)  # Mes/Año
    else:
        desde = datetime.min
        agrupado_por = func.strftime('%m/%Y', Service.datetime)

    datos = db.session.query(
        agrupado_por.label('fecha'),
        func.count(Service.id).label('cantidad')
    ).filter(Service.datetime >= desde).group_by('fecha').order_by('fecha').all()

    etiquetas = [fila.fecha for fila in datos]
    valores = [fila.cantidad for fila in datos]

    return jsonify({'labels': etiquetas, 'data': valores})
"""
