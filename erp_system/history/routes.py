from flask import Blueprint, render_template, request, jsonify
from erp_system.models import Service
from flask_login import login_required
from datetime import datetime, timedelta
from sqlalchemy import func
from erp_system import db


history_bp = Blueprint('history_bp',__name__)

@history_bp.route('/history')
@login_required
def history_page():
    return render_template('history.html')

@history_bp.route('/api/history_data')
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
