"""Creating the FastAPI app"""
from fastapi import FastAPI
from .router import build_router

def build_app():
    """
    Creates the FastAPI app
    """
    app = FastAPI()
    app.include_router(build_router())
    return app