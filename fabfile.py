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


@command
def deploy():
    with cd('opteacher'):
        with verbose("Connecting") as v:
            v.run('source ./venv/bin/activate')

        with verbose("Discarding local changes") as v:
            v.run('git reset HEAD; git clean -fd; git checkout .')

        with verbose("Pulling source code") as v:
            v.run('git pull')

        with verbose("Installing requirements") as v:
            v.run('pip install -r requirements.txt')

        with verbose("Starting") as v:
            v.run('fab start')
