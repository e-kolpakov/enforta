from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import run, sudo
from fabfile import virtualenv, get_environment


def run_db_script(script, db, user="postgres"):
    sudo("psql -d {0} -f {1}".format(db, script), user=user)


@task
def create_db():
    environment = get_environment()
    scripts = ("create_db.sql", "grant_permissions.sql")
    with cd(environment.SITE_ROOT + "/deployment"):
        for script in scripts:
            run_db_script(script, environment.DB)


@task
def migrate():
    environment = get_environment()

    with cd(environment.SITE_ROOT), virtualenv(environment.VENV):
        run("python ./manage.py syncdb && python ./manage.py migrate --all")