from contextlib import contextmanager
import os
from fabric.context_managers import prefix, shell_env, cd
from fabric.decorators import task
from fabric.state import env

__author__ = 'john'
git_repo = 'https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git'
virtualenv_location = '.virtualenvs'


class Environments:
    class Production:
        NAME = "production"
        USER_NAME = "enfortit"
        VENV = "DocApproval"
        SITE_NAME = "doc-approval"
        DB = "docapproval"
        BRANCH = "production"
        SITE_ROOT = os.path.join('/home', USER_NAME, SITE_NAME)
        LOGGING_DIRECTORY = os.path.join(SITE_ROOT, "log")
        MEDIA_ROOT = "/var/uploads/" + SITE_NAME
        LOG_OWNER_GROUP = "www-data"

    class Staging:
        NAME = "staging"
        USER_NAME = "enfortit"
        VENV = "DocApprovalStaging"
        SITE_NAME = "doc-approval-staging"
        DB = "docapproval_staging"
        BRANCH = "staging"
        SITE_ROOT = os.path.join('/home', USER_NAME, SITE_NAME)
        LOGGING_DIRECTORY = os.path.join(SITE_ROOT, "log")
        MEDIA_ROOT = "/var/uploads/" + SITE_NAME
        LOG_OWNER_GROUP = "www-data"

    class StagingLocal:
        NAME = "staging_local"
        USER_NAME = "john"
        VENV = "DocApprovalStaging"
        SITE_NAME = "doc-approval-staging"
        DB = "docapproval_staging"
        BRANCH = "staging"
        SITE_ROOT = os.path.join('/home', USER_NAME, SITE_NAME)
        LOGGING_DIRECTORY = os.path.join(SITE_ROOT, "log")
        MEDIA_ROOT = "/var/uploads/" + SITE_NAME
        LOG_OWNER_GROUP = "www-data"

    class Development:
        NAME = "development"
        USER_NAME = "john"
        VENV = "DocApproval"
        SITE_NAME = "doc-approval"
        DB = "docapproval"
        BRANCH = "master"
        SITE_ROOT = '/home/john/GitRoot/enforta'
        LOGGING_DIRECTORY = os.path.join(SITE_ROOT, "log")
        MEDIA_ROOT = "/var/uploads/" + SITE_NAME
        LOG_OWNER_GROUP = "www-data"


@task
def production():
    env.hosts = ['enfortit@87.241.226.36']
    env.environment = Environments.Production


@task
def staging():
    env.hosts = ['enfortit@87.241.226.36']
    env.environment = Environments.Staging


@task
def development():
    env.hosts = ['localhost']
    env.environment = Environments.Development


@task
def staging_local():
    env.hosts = ['localhost']
    env.environment = Environments.StagingLocal


@contextmanager
def virtualenv(environment_name):
    with prefix("source /usr/local/bin/virtualenvwrapper.sh && workon {0}".format(environment_name)):
        yield


@contextmanager
def set_environment(environment, local_dir=None):
    directory = os.path.join(environment.SITE_ROOT, local_dir) if local_dir else environment.SITE_ROOT
    with virtualenv(environment.VENV), cd(directory), \
         shell_env(SuppressLogging='true', EnvironmentType=environment.NAME):
        yield


def get_environment():
    if not hasattr(env, "environment"):
        available_envs = ("production", "staging", "development", "staging_local")
        message = "Configuration exception - must choose environment to run against. Available choices:\n{0}\n"
        envs = "\n".join("\t- " + env for env in available_envs)
        raise Exception(message.format(envs))
    return env.environment


import db
import provision
import prepare_deployment
import deploy