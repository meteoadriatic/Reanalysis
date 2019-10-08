# -*- coding: utf-8 -*-

"""The app module, containing the app factory function."""
from flask import Flask
from reanalysis import mod_public
from reanalysis.extensions import db


def create_app(config_object='reanalysis.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(mod_public.controllers.blueprint)
    return None
