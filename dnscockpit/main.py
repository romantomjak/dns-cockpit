import os

import jinja2
import aiohttp_jinja2
import aiohttp_security
import aiohttp_session
from aiohttp import web

from dnscockpit import views
from dnscockpit.adapters.database_auth import DatabaseAuthorizationPolicy
from dnscockpit.adapters.session_storage import PostgreSQLStorage
from dnscockpit.bootstrap import configure

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def app_factory(env):
    app = web.Application()
    app.add_routes([
        web.get('/', views.index, name='index'),
        web.get('/login', views.login, name='login'),
        web.post('/login', views.login, name='login'),
    ])
    app.router.add_static('/static/', path=os.path.join(BASE_DIR, 'static'), name='static')

    configure(app, env)

    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('dnscockpit', 'templates'))
    aiohttp_security.setup(app, aiohttp_security.SessionIdentityPolicy(), DatabaseAuthorizationPolicy(app))
    aiohttp_session.setup(app, PostgreSQLStorage())

    return app

web.run_app(app_factory(os.environ), host='127.0.0.1', port=8000)
