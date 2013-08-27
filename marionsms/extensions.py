# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt



db = SQLAlchemy()

lm = LoginManager()
lm.login_view = 'frontend.landing_page'

bcrypt = Bcrypt()
