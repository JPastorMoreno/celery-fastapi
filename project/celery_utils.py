import functools

from celery import current_app as current_celery_app
from celery import shared_task
from celery.result import AsyncResult
from project.config import settings


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY") #type: ignore

    return celery_app


def get_task_info(task_id):
    """
    return task info according to the task_id
    """
    task = AsyncResult(task_id)
    state = task.state

    if state == "FAILURE":
        error = str(task.result)
        response = {
            "state": task.state,
            "error": error,
        }
    else:
        response = {
            "state": task.state,
        }
    return response

class custom_celery_task:

    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            # you can add custom code here
            return func(*args, **kwargs)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func