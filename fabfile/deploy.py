from fabric.context_managers import shell_env
from fabric.decorators import task
from fabric.operations import run
from fabfile import get_environment, virtualenv_location, set_environment
from fabfile.db import migrate
from fabfile.provision import update_requirements, fetch_source_code


@task
def deploy():
    environment = get_environment()
    # prepare_deploy()
    with shell_env(WORKON_HOME=virtualenv_location), set_environment(environment):
        fetch_source_code(environment)
        run("git pull")
        update_requirements(environment)
        migrate()
        run("python ./manage.py collectstatic")
        run("touch portal/wsgi.py")