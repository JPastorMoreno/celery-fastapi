from celery import current_app as current_celery_app

from project.config import settings


# Rather than creating a new Celery instance, we used current_app so that shared tasks will work as expected.
def create_celery():
    celery_app = current_celery_app  # Factoy function that configures and then returns a Celery app
    celery_app.config_from_object(
        settings, namespace="CELERY"
    )  # means all celery-related configuration keys should be prefixed with CELERY_. For example, to configure the broker_url, we should use CELERY_BROKER_URL

    return celery_app
