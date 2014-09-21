from fabric.api import abort, local, quiet
from fabric.colors import blue, red


HOME_PATH = '/home/teacher/opteacher'
CONFIG_PATH = HOME_PATH + '/config/uwsgi.ini'
PID_PATH = HOME_PATH + '/var/opteacher.pid'


def command(f):
    def decorator(*args, **kwargs):
        with quiet():
            return f(*args, **kwargs)
    return decorator


def _abort(message):
    abort(red(message))


@command
def start():
    cmd = 'uwsgi %s --enable-threads' % CONFIG_PATH
    print blue("* Starting..."),
    rv = local(cmd, capture=True)
    if rv.succeeded:
        print blue("Done")
    else:
        print red("Failed")
        _abort(rv.stderr)


@command
def stop():
    print blue("* Stopping..."),
    stop_uwsgi = "uwsgi --stop %s" % PID_PATH
    rm_pid = "rm %s" % PID_PATH
    if local(stop_uwsgi).succeeded and local(rm_pid).succeeded:
        print blue("Done")
    else:
        print red("Failed")
