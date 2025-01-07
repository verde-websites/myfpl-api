"""Creating the FastAPI app"""
from fastapi import FastAPI
from .router import build_router
from .lifecycle import apschedule_lifespan
def build_app():
    """
    Creates the FastAPI app
    """
    app = FastAPI(lifespan=apschedule_lifespan)
    app.include_router(build_router())

    return app

