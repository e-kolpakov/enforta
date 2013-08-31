from fabric.api import local, settings, abort, cd, run, env, roles
from fabric.contrib.console import confirm


env.key_filename = '/path/to/keyfile.pem'
env.roledefs = {
    'production': ['enfortit@87.241.226.36']
}


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
    commit()
    push()


@roles("production")
def deploy():
    """deploys code"""
    code_dir = '/home/enfortit/docapproval2/'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone https://e_kolpakov@bitbucket.org/e_kolpakov/enforta.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch portal/wsgi.py")