from contextlib import contextmanager
from fabric.context_managers import prefix
from fabric.decorators import task
from fabric.state import env

__author__ = 'john'
git_repo = 'https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git'


class Environments:
    class Production:
        VENV = "DocApproval"
        SITE_ROOT = '/home/enfortit/docapproval/'
        DB = "docapproval"

    class Staging:
        VENV = "DocApprovalStaging"
        SITE_ROOT = '/home/enfortit/docapproval-staging/'
        DB = "docapproval-staging"

    class Development:
        VENV = "DocApproval"
        SITE_ROOT = '/home/john/GitRoot/Enforta/enforta/'
        DB = "docapproval"


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


def get_environment():
    if not hasattr(env, "environment"):
        available_envs = ("production", "staging", "development")
        message = "Configuration exception - must choose environment to run against. Available choices:\n{0}\n"
        envs = "\n".join("\t- " + env for env in available_envs)
        raise Exception(message.format(envs))
    return env.environment


@contextmanager
def virtualenv(environment_name):
    with prefix("source /usr/local/bin/virtualenvwrapper.sh && workon {0}".format(environment_name)):
        yield


import db
import deploy
import prepare_deployment
import provision