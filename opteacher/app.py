from flask import Flask

import parser

from views import blueprints


def create_app():
    app = Flask(__name__)
    app.debug = True
    register_blueprints(app)

    @app.before_request
    def before_request(*args, **kwargs):
        parser.parse_instruction_models(app)

    return app


def register_blueprints(app):
    for blueprint_name in blueprints:
        path = 'views.%s' % blueprint_name
        mod = __import__(path, fromlist=[blueprint_name])
        blueprint = getattr(mod, 'mod')
        app.register_blueprint(blueprint)


if __name__ == '__main__':
    create_app().run('0.0.0.0', 8000)
