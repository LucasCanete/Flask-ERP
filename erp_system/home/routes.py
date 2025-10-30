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


@home_bp.route("/logout")
def logout():
    logout_user()
    return(redirect(url_for('login_bp.login_page')))
