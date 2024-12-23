from datetime import datetime
import sys
import asyncio
import os
from logging.config import fileConfig
from alembic import context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.settings import get_settings

from src.database import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_settings().database_url
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
    configuration["sqlalchemy.url"] = get_settings().database_url

    connectable = async_engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await do_run_migrations(connection)
      #  await seed_database(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())