from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import sudo
from fabric.api import cd, run
from fabric.state import env

from fabfile.db import migrate
from fabfile.prepare_deployment import prepare_deploy


def restart_server():
    sudo("apache2ctl restart")


@task
def deploy():
    environment = env.environment
    site_dir, virtualenv = environment.SITE_ROOT, environment.VENV
    prepare_deploy()
    with settings(warn_only=True):
        if run("test -d %s" % site_dir).failed:
            run("git clone https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git %s" % site_dir)
    with cd(site_dir):
        run("git pull")
        run("touch portal/wsgi.py")
    migrate()
    restart_server()