from fabric.context_managers import shell_env
from fabric.decorators import task
from fabric.operations import sudo, run
from fabfile import get_environment


def provisioned():
    return False


def install_packages():
    """Installs required OS packages"""
    sudo("apt-get -y install git")
    sudo("apt-get -y install apache2 libapache2-mod-wsgi")
    sudo("apt-get -y install postgresql postgresql-client postgresql-server-dev-9.1")
    sudo("apt-get -y install python-pip python2.7-dev")
    sudo("apt-get -y install libffi-dev libxml2-dev libxslt-dev")


def install_virtualenv():
    sudo("pip install virtualenv")
    sudo("pip install virtualenvwrapper")


def make_virtualenv(environment):
    with shell_env(WORKON_HOME='.virtualenvs'):
        run("source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --no-site-packages %s" % environment.VENV)


def grant_webserver_permissions():
    pass

#     LOG_PATH=/home/enfortit/docapproval/log
# UPLOAD_PATH=/var/uploads/doc-approval
# sudo mkdir -p $LOG_PATH && sudo chown -R enfortit:www-data $LOG_PATH && sudo chmod g+ws -R $LOG_PATH
# sudo mkdir -p $UPLOAD_PATH && sudo chown www-data $UPLOAD_PATH && sudo chmod 775 $UPLOAD_PATH


@task
def provision():
    """ Provisions initial installation"""
    environment = get_environment()
    install_packages()
    install_virtualenv()
    make_virtualenv(environment)