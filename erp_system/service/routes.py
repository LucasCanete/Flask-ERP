from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from erp_system.forms import ServiceForm
from erp_system.models import Service
from erp_system import db
from datetime import datetime
from collections import defaultdict




service_bp = Blueprint('service_bp',__name__)


@service_bp.route("/")
@login_required
def services_page():
    #send_pdf_job()

    status_filter = request.args.get("status")
    date_filter = request.args.get("date")
    services = Service.query

    if status_filter:
        services = services.filter_by(status=status_filter)

    if date_filter:
        selected_date = datetime.strptime(date_filter, "%Y-%m-%d")
        start_datetime = selected_date
        end_datetime = selected_date + timedelta(days=1)  # exclusivo
        services = services.filter(Service.datetime >= start_datetime,
                               Service.datetime < end_datetime)

    services = services.order_by(Service.datetime.desc()).all()
    #group by day
    grouped = defaultdict(list)

    for service in services:
        day_str = service.datetime.strftime("%d/%m/%Y")
        grouped[day_str].append(service)

    # Convertir a lista de tuplas ordenada por fecha (reciente primero)
    grouped_services = sorted(grouped.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=True)

    return render_template("services.html", title="Servicios", grouped_services=grouped_services)


#update status in real time from the drop down menu
@service_bp.route("/update_status/<int:service_id>", methods=['POST'])
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


@service_bp.route("/service", methods=["GET","POST"])
@login_required
def create_service_page():
    form = ServiceForm()

    if form.validate_on_submit():
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        service = Service( type=form.type.data, client_name = form.client_name.data, client_address=form.client_address.data, client_phone=form.client_phone.data, status='En proceso', comment=form.comment.data)
        db.session.add(service)
        db.session.commit()
        flash(f'Nuevo servicio ha sido creado!','success')
        return redirect(url_for('service_bp.services_page'))

    return render_template("create_service.html", title="Servicio", form=form)


@service_bp.route("/edit_service/<id>", methods=['GET', 'POST'])
@login_required
def edit_service_page(id):
    form = ServiceForm()
    service = Service.query.filter_by(id=id).first()

    if not service:
        flash("Servicio no encontrado.", "danger")
        return redirect(url_for("home_bp.home_page"))

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
        return redirect(url_for("service_bp.services_page"))

    return render_template("edit_service.html", title="Editar Servicio", form=form, service=service )


@service_bp.route("/delete_service/<id>", methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.filter_by(id=id).first()

    if service:
        db.session.delete(service)
        db.session.commit()
        flash('Servicio eliminado correctamente.', 'success')

    else:
        flash('Servicio no encontrado.', 'danger')

    return redirect(url_for("service_bp.services_page"))
