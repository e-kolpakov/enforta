from contextlib import contextmanager
from fabric.context_managers import prefix
from fabric.decorators import task
from fabric.state import env

__author__ = 'john'
git_repo = 'https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git'


class Environments:
    class Production:
        NAME = "production"
        VENV = "DocApproval"
        SITE_ROOT = '/home/enfortit/docapproval/'
        SITE_NAME = "doc-approval"
        DB = "docapproval"
        BRANCH = "production"
        LOG_OWNER_USER = "enfortit"
        LOG_OWNER_GROUP = "www-data"
        APACHE_SITE_CONF = "production"

    class Staging:
        NAME = "staging"
        VENV = "DocApprovalStaging"
        SITE_ROOT = '/home/enfortit/docapproval-staging/'
        SITE_NAME = "doc-approval"
        DB = "docapproval_staging"
        BRANCH = "staging"
        LOG_OWNER_USER = "enfortit"
        LOG_OWNER_GROUP = "www-data"
        APACHE_SITE_CONF = "staging"

    class StagingLocal:
        NAME = "staging_local"
        VENV = "DocApprovalStaging"
        SITE_ROOT = '/home/john/docapproval-staging/'
        SITE_NAME = "doc-approval"
        DB = "docapproval_staging"
        BRANCH = "staging"
        LOG_OWNER_USER = "john"
        LOG_OWNER_GROUP = "www-data"
        APACHE_SITE_CONF = "staging_local"

    class Development:
        NAME = "development"
        VENV = "DocApproval"
        SITE_ROOT = '/home/john/GitRoot/Enforta/enforta/'
        SITE_NAME = "doc-approval"
        DB = "docapproval"
        BRANCH = "production"
        LOG_OWNER_USER = "john"
        LOG_OWNER_GROUP = "www-data"
        APACHE_SITE_CONF = "development"


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


def get_environment():
    if not hasattr(env, "environment"):
        available_envs = ("production", "staging", "development", "staging_local")
        message = "Configuration exception - must choose environment to run against. Available choices:\n{0}\n"
        envs = "\n".join("\t- " + env for env in available_envs)
        raise Exception(message.format(envs))
    return env.environment


import db
import deploy
import prepare_deployment