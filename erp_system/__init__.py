from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask import request
from erp_system.utils.wifi import is_connected
import os



#basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(os.getcwd(),'site.db')


app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"
#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_bp.login_page'


#helper template that separates number every 3 digits
@app.template_filter()
def currency(value):
    return f"{value:,}".replace(",", ".")


#from erp_system import routes
#IMPORT BLUEPRINT INSTANCE OF HOME PAGE
from erp_system.home.routes import home_bp
app.register_blueprint(home_bp)


#IMPORT BLUEPRINT INSTANCE OF LOGIN PAGE
from erp_system.login.routes import login_bp
app.register_blueprint(login_bp)


#IMPORT BLUEPRINT INSTANCE OF REGISTER PAGE
from erp_system.register.routes import register_bp
app.register_blueprint(register_bp)


#IMPORT BLUEPRINT INSTANCE OF SERVICE PAGE
from erp_system.service.routes import service_bp
app.register_blueprint(service_bp, url_prefix='/services')


#IMPORT BLUEPRINT INSTANCE OF SALE PAGE
from erp_system.sales.routes import sale_bp
app.register_blueprint(sale_bp, url_prefix='/sales')


#IMPORT BLUEPRINT INSTANCE OF HISTORY PAGE
from erp_system.history.routes import history_bp
app.register_blueprint(history_bp)


#IMPORT BLUEPRINT INSTANCE OF DOWNLOAD PAGE
from erp_system.download.routes import download_bp
app.register_blueprint(download_bp)


#IMPORT BLUEPRINT INSTANCE OF DOWNLOAD PAGE
from erp_system.connection.routes import connection_bp
app.register_blueprint(connection_bp)


#redirect automatically to connection page if it is not connected or another page is trying to be accesed
@app.before_request
def check_wifi_connection():
    # Evitar bucle infinito si ya estamos en la página de conexión
    if request.endpoint != "connection_bp.connection_page" and not is_connected():
        return redirect(url_for("connection_bp.connection_page"))
