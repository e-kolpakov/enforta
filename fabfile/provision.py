import sys
import logging
from django.core.exceptions import ImproperlyConfigured
from fabric.decorators import task, with_settings
from fabric.api import cd, run
from fabric.context_managers import shell_env, settings
from fabric.contrib import django
from fabric.operations import sudo, os
from django.conf import settings as django_settings

from fabfile import get_environment, git_repo, set_environment, virtualenv_location
from fabfile.db import create_db
from fabfile.supervisor import configure as configure_supervisor

logger = logging.getLogger(__name__)


def prepare_django_conf(environment):
    local_project_path = (os.path.sep).join(os.path.dirname(__file__).split(os.path.sep)[0:-1])
    sys.path.append(environment.SITE_ROOT)
    sys.path.append(local_project_path)
    os.environ['SuppressLogging'] = 'true'  # only key existense is checked
    os.environ['EnvironmentType'] = environment.NAME
    django.project('portal')


def activate_site(site_name="doc-approval"):
    sudo("a2ensite {0}".format(site_name))


def deactivate_site(site_name="doc-approval"):
    sudo("a2dissite {0}".format(site_name))


def restart_server():
    sudo("apache2ctl restart")


@task
def install_packages():
    """Installs required OS packages"""
    sudo("apt-get -y install git")
    sudo("apt-get -y install apache2 libapache2-mod-wsgi")
    sudo("apt-get -y install postgresql postgresql-client postgresql-server-dev-9.1")
    sudo("apt-get -y install python-pip python2.7-dev")
    sudo("apt-get -y install libffi-dev libxml2-dev libxslt-dev")
    sudo("apt-get -y install rabbitmq-server")
    sudo("apt-get -y install supervisor")


def install_virtualenv():
    sudo("pip install virtualenv")
    sudo("pip install virtualenvwrapper")


def create_virtualenv(environment):
    with shell_env(WORKON_HOME=virtualenv_location):
        run("source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv %s" % environment.VENV)


def fetch_source_code(environment):
    with settings(warn_only=True):
        result = run("test -d {0}".format(environment.SITE_ROOT))
    if result.failed:
        run("mkdir {0}".format(environment.SITE_ROOT))
        run("git clone {0} -b {1} {2}".format(git_repo, environment.BRANCH, environment.SITE_ROOT))
    else:
        with cd(environment.SITE_ROOT):
            run("git pull")


@task
def update_requirements(environment=None):
    environment = environment if environment else get_environment()
    with set_environment(environment, local_dir="deployment"):
        run("pip install -r requirements.txt")


@task
def create_log_and_upload_folders(environment=None):
    environment = environment if environment else get_environment()
    log_files = ('django.log', 'sql.log', 'celery.log')
    log_tpl = "mkdir -p {0} && chown -R {1}:{2} {0} && sudo chmod 777 -R {0}"
    upload_tpl = "sudo mkdir -p {0} && sudo chown {1}:{2} {0} && sudo chmod 775 {0}"
    sudo(log_tpl.format(environment.LOGGING_DIRECTORY, environment.USER_NAME, environment.LOG_OWNER_GROUP))
    sudo(upload_tpl.format(environment.MEDIA_ROOT, environment.USER_NAME, environment.LOG_OWNER_GROUP))

    tpl = "touch {0}/{1} && chmod 666 {0}/{1}"
    for log_file in log_files:
        sudo(tpl.format(environment.LOGGING_DIRECTORY, log_file), user=environment.USER_NAME)


@task
def init_south(environment=None):
    environment = environment if environment else get_environment()
    apps_to_migrate = ('DocApproval', 'DocApprovalNotifications', 'reversion', 'guardian', 'djcelery')
    with set_environment(environment):
        for app in apps_to_migrate:
            run("python ./manage.py migrate {0}".format(app))


def load_initial_fixtures(environment):
    with set_environment(environment):
        run("python ./manage.py loaddata start_data.yaml")


@task
def configure_apache(environment=None):
    environment = environment if environment else get_environment()
    with set_environment(environment, local_dir="deployment/apache-conf"):
        sudo("cp {0} /etc/apache2/sites-available/{1}".format(environment.NAME, environment.SITE_NAME))
        deactivate_site(environment.SITE_NAME)
        activate_site(environment.SITE_NAME)
        deactivate_site("default")
        restart_server()


@task
@with_settings(warn_only=True)
def configure_rabbitmq(environment=None):
    environment = environment if environment else get_environment()
    try:
        user, password, host = django_settings.AMQP_USER, django_settings.AMQP_PASS, django_settings.AMQP_HOST
    except ImproperlyConfigured:
        logger.warning("Django settings were not configured, configuring using {environment}", environment.NAME)
        prepare_django_conf(environment)
        user, password, host = django_settings.AMQP_USER, django_settings.AMQP_PASS, django_settings.AMQP_VHOST
    command = 'rabbitmqctl add_user {user} {password} && rabbitmqctl add_vhost {host} && rabbitmqctl set_permissions -p {host} {user} ".*" ".*" ".*"'
    sudo(command.format(user=user, password=password, host=host))


@task
def provision():
    """ Provisions initial installation"""
    environment = get_environment()
    install_packages()
    install_virtualenv()
    create_virtualenv(environment)
    fetch_source_code(environment)
    update_requirements(environment)
    prepare_django_conf(environment)
    create_log_and_upload_folders(environment)
    create_db(environment)
    init_south(environment)
    load_initial_fixtures(environment)
    configure_apache(environment)
    configure_rabbitmq()
    configure_supervisor(environment)