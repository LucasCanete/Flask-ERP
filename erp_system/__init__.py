from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask import request
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
app.register_blueprint(service_bp)


#IMPORT BLUEPRINT INSTANCE OF HISTORY PAGE
from erp_system.history.routes import history_bp
app.register_blueprint(history_bp)

#IMPORT BLUEPRINT INSTANCE OF SALE PAGE
from erp_system.sales.routes import sale_bp
app.register_blueprint(sale_bp)
