from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
#configuro base de datos
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#configuro login
login = LoginManager(app)
#funcion de flask-login pra redirigir usuarios no registrados a /login si tratan de ver view protegido
login.login_view = 'login'

from app import routes, models