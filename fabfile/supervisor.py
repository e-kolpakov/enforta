from StringIO import StringIO
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import sudo, os, put
from fabfile import get_environment, virtualenv_location


def build_config(tpl, environment):
    python_exec = os.path.join("/home", environment.USER_NAME, virtualenv_location, environment.VENV, "bin/python")
    return StringIO(tpl.format(
        site_root=environment.SITE_ROOT,
        python_exec=python_exec,
        user=environment.USER_NAME,
        env_type=environment.NAME
    ))


@task(alias='svdconf')
def configure(environment=None):
    configs = ("celery", 'celerybeat')
    local_tpl_location = os.path.join(os.path.dirname(__file__), "../config")
    environment = environment if environment else get_environment()
    print(local_tpl_location)
    with cd(os.path.join(environment.SITE_ROOT, "config")):
        for config in configs:
            remote_file = config + ".conf"
            with open(os.path.join(local_tpl_location, config + "_tpl.conf"), "r") as template_file:
                tpl = template_file.read()
            put(build_config(tpl, environment), remote_file)
            sudo("cp {filename} /etc/supervisor/conf.d/{filename}".format(filename=remote_file))

    sudo("service supervisor stop && sleep 2s && service supervisor start")
