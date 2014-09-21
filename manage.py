from flask.ext.script import Manager

from opteacher import ext, parser
from opteacher.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def initdb():
    ext.db.drop_all()
    ext.db.create_all(app=app)
    parser.parse_instruction_models(app)


@manager.command
def run():
    initdb()
    app.debug = True
    app.run('0.0.0.0', 8000)


if __name__ == '__main__':
    manager.run()
