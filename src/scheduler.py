from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import pytz
from .database import engine  # Reuse your database setup

# Initialize the scheduler
scheduler = AsyncIOScheduler()

scheduler.add_jobstore(SQLAlchemyJobStore(engine=engine.sync_engine), alias="default")
scheduler.add_executor(ThreadPoolExecutor(max_workers=20), alias="default")
scheduler.job_defaults = {
    "coalesce": False,
    "max_instances": 3
}
scheduler.configure(timezone=pytz.timezone("UTC"))

