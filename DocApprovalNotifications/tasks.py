from celery import task


@task()
def send_immediate_notifications():
    return 10