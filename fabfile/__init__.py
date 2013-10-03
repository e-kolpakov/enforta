from fabric.decorators import task
from fabric.state import env

__author__ = 'john'
git_repo = 'https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git'


class Environments:
    class Production:
        VENV = "DocApproval"
        SITE_ROOT = '/home/enfortit/docapproval/'

    class Staging:
        VENV = "DocApprovalStaging"
        SITE_ROOT = '/home/enfortit/docapproval-staging/'

    class Development:
        VENV = "DocApproval"
        SITE_ROOT = '/home/john/GitRoot/Enforta/enforta/'


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


import db
import deploy
import prepare_deployment
import provision