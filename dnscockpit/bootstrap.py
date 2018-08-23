import logging
import logging.config
from functools import partial

import asyncpg
import inject

from dnscockpit import config
from dnscockpit.orm import orm
from dnscockpit.orm.context_managers import ConnectionManager


async def bootstrap(env):
    configure_logging(env)

    dsn = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(**config.get_db_config(env))

    sa = orm.SQLAlchemy(dsn)
    sa.configure_mappings()
    sa.create_all_tables()

    pool = await init_pg_pool(dsn)
    db = ConnectionManager(pool)

    binder_config = partial(configure_binder, pool, db)
    inject.configure(binder_config)


def configure_logging(env):
    cfg = config.get_logging_config(env)
    logging.config.dictConfig(cfg)


async def init_pg_pool(dsn):
    logging.debug("Initialising DB pool")
    return await asyncpg.create_pool(dsn)


def configure_binder(pool, db, binder):
    binder.bind('pool', pool)
    binder.bind('db', db)
