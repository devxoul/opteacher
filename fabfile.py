from fabric.api import cd, env, quiet
from fabric_verbose import verbose


env.hosts = ['teacher@xoul.kr']


HOME_PATH = '/home/teacher/opteacher'
CONFIG_PATH = HOME_PATH + '/config/uwsgi.ini'
PID_PATH = HOME_PATH + '/var/uwsgi.pid'


def command(f):
    def decorator(*args, **kwargs):
        with quiet():
            return f(*args, **kwargs)
    return decorator


def venv(command):
    return 'source ./venv/bin/activate && %s' % command


@command
def start():
    with verbose("Starting") as v:
        v.local('uwsgi %s --enable-threads' % CONFIG_PATH)


@command
def stop():
    with verbose("Stopping") as v:
        v.local("uwsgi --stop %s" % PID_PATH)

    with verbose("Removing pid file") as v:
        v.local("rm %s" % PID_PATH)

    with verbose("Killing progress") as v:
        v.local("ps aux | grep %s | awk '{print $2}' | "
                "xargs kill -9 2>/dev/null" % CONFIG_PATH)


@command
def deploy(req=False):
    with cd('opteacher'):
        with verbose("Connecting") as v:
            v.run('source ./venv/bin/activate')

        with verbose("Discarding local changes") as v:
            v.run('git reset HEAD; git clean -fd; git checkout .')

        with verbose("Pulling source code") as v:
            v.run('git fetch origin')
            v.run('git checkout master')
            v.run('git reset --hard origin/master')

        with verbose("Installing requirements") as v:
            v.run(venv('pip install -r requirements.txt'))

        with verbose("Initializing database") as v:
            v.run(venv('python manage.py initdb'))

        with verbose("Starting") as v:
            v.run(venv('fab stop'))
            v.run(venv('fab start'))
