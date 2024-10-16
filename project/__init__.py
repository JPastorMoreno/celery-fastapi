from fastapi import FastAPI

from project.celery_utils import create_celery


def create_app() -> FastAPI:
    app = FastAPI()

    # do this before loading routes
    app.celery_app = create_celery()
    from project.users import (
        users_router,  # When this is called, the code in project/uisers/__init__.py will run, and models.py will be imported as well
    )

    app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
