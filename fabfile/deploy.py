from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import sudo
from fabric.api import cd, run, roles

from fabfile.db import migrate
from fabfile.prepare_deployment import prepare_deploy
from fabfile.provision import provision, provisioned


__all__ = ['deploy_production', 'deploy_staging']


def restart_server():
    sudo("apache2ctl restart")


def do_deploy(local_dir):
    prepare_deploy()
    if not provisioned():
        provision()
    with settings(warn_only=True):
        if run("test -d %s" % local_dir).failed:
            run("git clone https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git %s" % local_dir)
    with cd(local_dir):
        run("git pull")
        run("touch portal/wsgi.py")
    migrate()
    restart_server()


@task
@roles("production")
def deploy_production():
    """deploys code"""
    do_deploy('/home/enfortit/docapproval/')


@task
@roles("staging")
def deploy_staging():
    do_deploy('/home/enfortit/docapproval-staging/')