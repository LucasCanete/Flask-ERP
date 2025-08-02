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
login_manager.login_view = 'login_page'



from erp_system import routes
