from StringIO import StringIO
from fabric.context_managers import cd, settings
from fabric.decorators import task
from fabric.operations import run, sudo, put
from fabfile import get_environment, set_environment

create_db_tpl = """
CREATE ROLE sa SUPERUSER LOGIN CREATEDB PASSWORD 'sa!v3ry_str0ng_p@ssw0rd#!';
CREATE ROLE DocApprovalUser LOGIN PASSWORD 'dau!w3aker_p@ssword';
CREATE DATABASE {db_name};
GRANT CONNECT ON DATABASE DocApproval TO DocApprovalUser;
GRANT ALL ON DATABASE DocApproval TO sa;
"""


@task
def create_db(environment=None):
    env = environment if environment else get_environment()
    with cd(env.SITE_ROOT + "/deployment"):
        put(StringIO(create_db_tpl.format(db_name=env.DB)), "create_db.sql")
        with settings(warn_only=True):
            sudo("psql -f {0}".format("create_db.sql"), user="postgres")
        sudo("psql -d {1} -f {0}".format("grant_permissions.sql", env.DB), user="postgres")
    with set_environment(environment):
        run("python ./manage.py syncdb")


@task
def migrate(environment=None):
    env = environment if environment else get_environment()
    with set_environment(env):
        run("python ./manage.py syncdb && python ./manage.py migrate --all")
        sudo("psql -d {1} -f {0}".format("deployment/grant_permissions.sql", env.DB), user="postgres")