from __future__ import with_statement
import os

from alembic import context
from sqlalchemy import create_engine, MetaData

from dnscockpit import config, bootstrap
from dnscockpit.orm import mappings

bootstrap.configure_logging(os.environ)

dsn = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(**config.get_db_config(os.environ))
target_metadata = mappings.configure_mappings(MetaData())


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=dsn, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(dsn)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
