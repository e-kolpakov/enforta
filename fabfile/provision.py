from fabric.decorators import task


@task
def provisioned():
    return False


@task
def provision():
    pass