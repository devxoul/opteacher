from flask import Flask

from opteacher import config, ext
from opteacher.views import blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    ext.init_db(app)
    return app


def register_blueprints(app):
    for blueprint_name in blueprints:
        path = 'opteacher.views.%s' % blueprint_name
        mod = __import__(path, fromlist=[blueprint_name])
        blueprint = getattr(mod, 'mod')
        app.register_blueprint(blueprint)
