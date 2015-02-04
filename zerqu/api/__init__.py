# coding: utf-8


from .base import ratelimit_hook
from . import base, users


def register_blueprint(app, bp):
    bp.after_request(ratelimit_hook)
    app.register_blueprint(bp, url_prefix='/api')


def init_app(app):
    register_blueprint(app, base.bp)
    register_blueprint(app, users.bp)
