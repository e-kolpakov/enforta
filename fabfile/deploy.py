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
    configure_apache()
    with cd(environment.SITE_ROOT):
        run("touch portal/wsgi.py")


@task
def configure_apache(site_name="doc-approval"):
    environment = get_environment()
    with cd(environment.SITE_ROOT + "/deployment"):
        sudo("cp {0} /etc/apache2/sites-available/{1}".format(environment.APACHE_SITE_CONF, site_name))
        deactivate_site(site_name)
        activate_site(site_name)
        deactivate_site("default")
        sudo("apache2ctl restart")


@task
def activate_site(site_name="doc-approval"):
    sudo("a2ensite {0}".format(site_name))


@task
def deactivate_site(site_name="doc-approval"):
    sudo("a2dissite {0}".format(site_name))