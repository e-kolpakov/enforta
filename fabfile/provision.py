import re
import sys
import logging

from django.core.exceptions import ImproperlyConfigured
from fabric.decorators import task, with_settings
from fabric.api import cd, run
from fabric.context_managers import shell_env, settings
from fabric.contrib import django
from fabric.operations import sudo, os
from django.conf import settings as django_settings
from fabric.utils import abort

from fabfile import get_environment, git_repo, set_environment, virtualenv_location
from fabfile.db import create_db
from fabfile.supervisor import configure as configure_supervisor

logger = logging.getLogger(__name__)

@task
@with_settings(warn_only=True)
def get_apache_version():
    apache_ver_query = run("apache2ctl -V | grep Apache/2").split("\n")
    regex = re.compile("Apache/(\d)\.(\d+)\.(\d+)")
    for line in apache_ver_query:
        match = regex.search(line)
        if match:
            return {'major': int(match.group(1)), 'minor': int(match.group(2)), 'build': int(match.group(3))}
    return {'major': 2, 'minor': 2, 'build': 22}


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


def install_mod_wsgi3_4():
    """
     mod_wsgi 3.4 required for this application, Ubuntu 12.04 have 3.3 in repositories.
     That's why in order to run it on Ubuntu 12.04 manual upgrade to 3.4 is required.
     At production server this was done long before fabric was introduced, that's why this method is only a stub.
    """
    pass


def install_virtualenv():
    sudo("pip install virtualenv")
    sudo("pip install virtualenvwrapper")


def create_virtualenv(environment):
    with settings(warn_only=True):
        venv_location = os.path.join("/home", environment.USER_NAME, virtualenv_location, environment.VENV)
        result = run("test -d {0}".format(venv_location))
    if result.failed:
        with shell_env(WORKON_HOME=virtualenv_location):
            run("source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv %s" % environment.VENV)

@task
def fetch_source_code(environment=None):
    environment = environment if environment else get_environment()
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
    log_tpl = "mkdir -p {0} && chown -R {1}:{2} {0} && sudo chmod 775 -R {0}"
    upload_tpl = "sudo mkdir -p {0} && sudo chown {1}:{2} {0} && sudo chmod 775 {0}"
    sudo(log_tpl.format(environment.LOGGING_DIRECTORY, environment.USER_NAME, environment.LOG_OWNER_GROUP))
    sudo(upload_tpl.format(environment.MEDIA_ROOT, environment.USER_NAME, environment.LOG_OWNER_GROUP))

    with settings(warn_only=True):
        result = run("test -d /var/log/celery")
    if result.failed:
        sudo("mkdir /var/log/celery && chmod 755 /var/log/celery")

    tpl = "touch {0}/{1} && chmod 664 {0}/{1}"
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
    suffix = '.conf'
    apache_ver = get_apache_version()
    if apache_ver['major'] == 2 and apache_ver['minor'] <= 2:
        suffix = ''
    with set_environment(environment, local_dir="deployment/apache-conf"):
        sudo("cp {0} /etc/apache2/sites-available/{1}{2}".format(environment.NAME, environment.SITE_NAME, suffix))
        with settings(warn_only=True):
            deactivate_site(environment.SITE_NAME)
        activate_site(environment.SITE_NAME)
        with settings(warn_only=True):
            deactivate_site("*default")
        restart_server()


@task
def configure_rabbitmq(environment=None):
    environment = environment if environment else get_environment()
    try:
        user = django_settings.AMQP_USER
    except ImproperlyConfigured:
        logger.warning("Django settings were not configured, configuring using {environment}", environment.NAME)
        prepare_django_conf(environment)
    user, password, host = django_settings.AMQP_USER, django_settings.AMQP_PASS, django_settings.AMQP_VHOST
    with settings(warn_only=True):
        result = sudo("rabbitmqctl add_user {user} {password}".format(user=user, password=password))
        if result.failed and not 'user_already_exists' in result:
            abort(result)
        sudo("rabbitmqctl add_vhost {host}".format(host=host))
        sudo('rabbitmqctl set_permissions -p {host} {user} ".*" ".*" ".*"'.format(user=user, host=host))


@task
def provision():
    """ Provisions initial installation"""
    environment = get_environment()
    install_packages()
    install_mod_wsgi3_4()
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
    configure_rabbitmq(environment)
    configure_supervisor(environment)