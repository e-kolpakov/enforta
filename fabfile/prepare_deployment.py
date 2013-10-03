from fabric.decorators import task
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm


@task
def test():
    with settings(warn_only=True):
        result = local("./manage.py test DocApproval")
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


@task
def commit():
    with settings(warn_only=True):
        result = local("git checkout master && git add -p && git commit")
    if result.failed and not confirm("Nothing to commit. Continue anyway?"):
        abort("Aborting at user request.")


@task
def push():
    local("git push")


@task
def prepare_deploy():
    """prepares code to be deployed"""
    # test()
    commit()
    push()
