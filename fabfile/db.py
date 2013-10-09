from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import run, sudo
from fabfile import virtualenv, get_environment


def run_db_script(script, db, user="postgres"):
    sudo("psql -d {0} -f {1}".format(db, script), user=user)


@task
def create_db(environment=None):
    env = environment if environment else get_environment()
    scripts = ("create_db.sql", "grant_permissions.sql")
    with cd(env.SITE_ROOT + "/deployment"):
        for script in scripts:
            run_db_script(script, environment.DB)


@task
def migrate(environment=None):
    env = environment if environment else get_environment()
    with cd(env.SITE_ROOT), virtualenv(env.VENV):
        run("python ./manage.py syncdb && python ./manage.py migrate --all")
        run_db_script("grant_permissions.sql", environment.DB)