from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from erp_system.forms import ServiceForm
from erp_system.models import Service
from erp_system import db
from datetime import datetime



service_bp = Blueprint('service_bp',__name__)

@service_bp.route("/service", methods=["GET","POST"])
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
        return redirect(url_for('home_bp.home_page'))
    return render_template("service.html", title="Servicio", form=form)

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
        return redirect(url_for("home_bp.home_page"))

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
    return redirect(url_for("home_bp.home_page"))
