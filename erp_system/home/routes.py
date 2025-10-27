from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from erp_system import db
from erp_system.models import Service
from flask_login import login_required, logout_user
from datetime import datetime, timedelta
from collections import defaultdict

home_bp = Blueprint('home_bp',__name__)

@home_bp.route("/")
@login_required
def home_page():
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

    return render_template("home.html", title="Servicios", grouped_services=grouped_services)


#update status in real time from the home page via drop down menu
@home_bp.route("/update_status/<int:service_id>", methods=['POST'])
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


@home_bp.route("/logout")
def logout():
    logout_user()
    return(redirect(url_for('login_bp.login_page')))
