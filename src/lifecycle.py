from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.scheduler import scheduler

@asynccontextmanager
async def apschedule_lifespan(app: FastAPI):
    print("Starting APScheduler")
    # Configure APScheduler
    scheduler.start()
    yield
    print("Shutting down APScheduler")
    scheduler.shutdown()