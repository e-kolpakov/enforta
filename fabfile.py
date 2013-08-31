from fabric.api import local, settings, abort, cd, run
from fabric.contrib.console import confirm


def test():
    with settings(warn_only=True):
        result = local("./manage.py test DocApproval")
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def commit():
    local("git add -p && git commit")


def push():
    local("git push")


def prepare_deploy():
    """prepares code to be deployed"""
    # test()
    # commit()
    # push()


def deploy():
    """deploys code"""
    code_dir = '/home/john/enforta/'
    code_dir = '/home/enfortit/enforta/'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")