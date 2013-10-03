from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import sudo
from fabric.api import cd, run
from fabfile import virtualenv, get_environment

from fabfile.db import migrate


def restart_server():
    sudo("apache2ctl restart")


@task
def update_requirements():
    environment = get_environment()
    with virtualenv(environment.VENV), cd(environment.SITE_ROOT + "/deployment"):
        run("pip install -r requirements.txt")


@task
def deploy():
    environment = get_environment()
    # prepare_deploy()
    with settings(warn_only=True):
        result = run("test -d %s" % environment.SITE_ROOT)
    if result.failed:
        run("mkdir %s" % environment.BRANCH)
        run("git clone https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git -b %s %s" % (
            environment.BRANCH, environment.SITE_ROOT))
    with cd(environment.SITE_ROOT):
        run("git pull")
    update_requirements()
    migrate()
    with cd(environment.SITE_ROOT):
        run("touch portal/wsgi.py")