# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask, session, render_template, current_app, request, redirect
from flask.ext.login import current_user
from werkzeug import url_decode
import pytz
from datetime import datetime


from .extensions import db, lm, bcrypt
from .middleware import MethodRewriteMiddleware

from .models import User

# Blueprints
from .frontend import frontend
from .api import api
from .sms import sms


BLUEPRINTS = (frontend, api, sms)


def create_app():
    app = Flask(__name__)

    _initialize_config(app)
    _initialize_middleware(app)
    _initialize_hooks(app)
    _initialize_extensions(app)
    _initialize_blueprints(app)
    _initialize_error_handlers(app)
    _initialize_logging(app)
    _initialize_template_filters(app)

    return app



def _initialize_config(app):
    app.config.from_object('config')


def _initialize_middleware(app):
    app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)


def _initialize_hooks(app):
    from urlparse import urlparse, urlunparse

    # @app.before_request
    # def redirect_nonhttps():
    #     """Redirect non-www requests to www."""
    #     if app.config.get('ENVIRONMENT') == 'PRODUCTION':
    #         urlparts = urlparse(request.url)
    #         if urlparts.scheme == 'http':
    #             urlparts_list = list(urlparts)
    #             urlparts_list[0] = 'https'
    #             urlparts_list[1] = 'www.getmarion.com'
    #             return redirect(urlunparse(urlparts_list), code=301)
    pass


def _initialize_extensions(app):
    db.init_app(app)
    lm.init_app(app)
    bcrypt.init_app(app)

    @lm.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # @lm.token_loader
    # def load_token(token):
    #     return User.query.get(int(token))


def _initialize_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def _initialize_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404


def _initialize_logging(app):
    if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
        stream_handler = logging.StreamHandler()
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)


def _initialize_template_filters(app):
    @app.template_filter()
    def fmt_time(dt):
        now = datetime.now()
        dt = datetime(now.year, now.month, now.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        ds = dt.strftime("%I:%M %p")
        return ds.lstrip('0')

    @app.template_filter()
    def format_phone_number(pn):
        fpn = ''
        fpn += pn[0:2]
        fpn += ' ('
        fpn += pn[2:5]
        fpn += ') '
        fpn += pn[5:8]
        fpn += '-'
        fpn += pn[8:12]
        
        return fpn

