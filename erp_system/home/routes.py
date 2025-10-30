from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from erp_system import db
from erp_system.models import Service
from flask_login import login_required, logout_user
from datetime import datetime, timedelta



'''
When First running to create db execute



from erp_system import db, app
app.app_context().push()
db.create_all()

This will create db inside instances
'''

home_bp = Blueprint('home_bp',__name__)



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
