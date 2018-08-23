import asyncio
import os
import logging

import aiohttp_jinja2
import aiohttp_security
import aiohttp_session
import inject
import jinja2
from aiohttp import web

from dnscockpit import views, config
from dnscockpit.auth import DatabaseAuthorizationPolicy
from dnscockpit.bootstrap import bootstrap
from dnscockpit.session import PostgreSQLStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def close_pg_pool(app):
    logging.debug("Closing DB pool")
    pool = inject.instance('pool')
    await asyncio.wait_for(pool.close(), 30.0)


async def app_factory(env):
    await bootstrap(env)

    app = web.Application()
    app.add_routes([
        web.get('/', views.index, name='index'),
        web.get('/login', views.login, name='login'),
        web.post('/login', views.login),
    ])
    app.router.add_static('/static/', path=os.path.join(BASE_DIR, 'static'), name='static')

    app.on_cleanup.append(close_pg_pool)

    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('dnscockpit', 'templates'))
    aiohttp_security.setup(app, aiohttp_security.SessionIdentityPolicy(), DatabaseAuthorizationPolicy())
    aiohttp_session.setup(app, PostgreSQLStorage())

    return app

web.run_app(app_factory(os.environ), **config.get_server_config(os.environ))
