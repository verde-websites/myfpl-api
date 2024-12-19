from datetime import datetime
import sys
import asyncio
import os
from logging.config import fileConfig

from alembic import context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models import Base, FPLScraperAccount
from src.database import sessionmanager
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL")

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def do_run_migrations(connection):
    await connection.run_sync(run_migrations)

def run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    print("REACHED")
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await do_run_migrations(connection)
      #  await seed_database(connection)

async def seed_database(engine):
    """Function to seed the database with an initial FPL manager session."""
    async with AsyncSession(engine) as session:
        # Check if there's already a seeded entry
        stmt = select(FPLScraperAccount).where(FPLScraperAccount.email == "example@example.com")
        result = await session.execute(stmt)
        existing_entry = result.scalars().first()
        #stmt = select(FPLScraperAccount).where(FPLScraperAccount.email == "example@example.com")
        #result = await session.execute(stmt)
        #existing_entry = result.scalars().first()

      #  existing_entry = await session.execute(
      #      session.query(FPLScraperAccount).filter_by(email="example@example.com")
      #  )

        # If no entry exists, insert one
        if not existing_entry:
            new_manager = FPLScraperAccount(
                email="yategip337@jucatyo.com",
                password="WL@+simEHnu8?m+",
                manager_id="80834613",
                cookies="",
                in_use=False,
                #last_used=datetime.utcnow(),
                #cookies_last_updated=datetime.utcnow(),
                active=True
            )
            session.add(new_manager)
            await session.commit()
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())