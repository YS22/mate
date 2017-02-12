from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.bootstrap import Bootstrap
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir




app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

lm = LoginManager()
lm.init_app(app)
# lm.login_view = 'http://162.243.128.84:90/login'
lm.login_view = 'login'

# bootstrap = Bootstrap(app)

from app import views,models