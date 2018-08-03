import asyncio
import logging.config
from functools import partial

import asyncpg

from dnscockpit import config


def configure(app, env):
    configure_logging(env)
    app.on_startup.append(partial(init_pg_pool, env))
    app.on_cleanup.append(close_pg_pool)


def configure_logging(env):
    cfg = config.get_logging_config(env)
    logging.config.dictConfig(cfg)


async def init_pg_pool(env, app):
    dsn = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(**config.get_db_config(env))
    pool = await asyncpg.create_pool(dsn)
    app['db'] = pool


async def close_pg_pool(app):
    await asyncio.wait_for(app['db'].close(), 30.0)
