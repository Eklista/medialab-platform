"""
Alembic environment configuration for Universidad Galileo MediaLab Platform
"""
import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import all models to ensure they're registered with SQLAlchemy
from app.shared.base.base_model import BaseModelWithID, BaseModelWithUUID, BaseModelHybrid

# Import all models from each module
from app.modules.security.models import Permission, Role, RolePermission
from app.modules.organizations.models import AcademicUnitType, AcademicUnit, Area
from app.modules.users.models import (
    BaseUser, InternalUser, InstitutionalUser, 
    UserRole, UserArea, UserAcademicUnit
)
from app.modules.cms.models import Category, Video, Gallery

# Import database configuration
from app.core.config import get_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get database URL from settings
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# add your model's MetaData objects here for 'autogenerate' support
# We need to combine metadata from all base models
target_metadata = []

# Add metadata from each base model
if hasattr(BaseModelWithID, 'metadata'):
    target_metadata.append(BaseModelWithID.metadata)
if hasattr(BaseModelWithUUID, 'metadata'):
    target_metadata.append(BaseModelWithUUID.metadata)
if hasattr(BaseModelHybrid, 'metadata'):
    target_metadata.append(BaseModelHybrid.metadata)

# Combine all metadata
from sqlalchemy import MetaData
combined_metadata = MetaData()
for metadata in target_metadata:
    for table in metadata.tables.values():
        table.tometadata(combined_metadata)

target_metadata = combined_metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_object(object, name, type_, reflected, compare_to):
    """
    Filter objects to include in migrations
    """
    # Skip alembic version table
    if type_ == "table" and name == "alembic_version":
        return False
    
    # Include all our tables
    return True


def compare_type(context, inspected_column, metadata_column, inspected_type, metadata_type):
    """
    Compare column types for autogenerate
    """
    # Handle MySQL specific type comparisons
    if context.dialect.name == "mysql":
        # Handle CHAR vs VARCHAR differences
        if hasattr(inspected_type, 'length') and hasattr(metadata_type, 'length'):
            if inspected_type.length == metadata_type.length:
                return False
    
    # Default comparison
    return None


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=compare_type,
        render_as_batch=True,  # For SQLite compatibility if needed
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    Run migrations with database connection
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        compare_type=compare_type,
        render_as_batch=True,  # For SQLite compatibility if needed
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations in async mode
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Check if we should run in async mode
    if config.get_main_option("sqlalchemy.url", "").startswith("mysql+aiomysql"):
        asyncio.run(run_async_migrations())
    else:
        # Synchronous mode
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()