import json
import time

import aiohttp_session
from aiohttp import web

from dnscockpit.auth import login_required


def make_cookie(client, data):
    session_data = {
        'session': data,
        'created': int(time.time())
    }
    value = json.dumps(session_data)
    client.session.cookie_jar.update_cookies({'AIOHTTP_SESSION': value})


def create_app():
    @login_required
    async def index(request):
        return web.Response(body=b'OK')

    async def login(request):
        return web.Response(body=b'OK')

    app = web.Application()
    app.router.add_route(method='GET', path='/', handler=index, name='index')
    app.router.add_route(method='GET', path='/login', handler=login, name='login')
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())

    return app


async def test_unauthorized_user_is_redirected_to_login_page(aiohttp_client):
    client = await aiohttp_client(create_app())

    resp = await client.get('/')
    assert resp.url == client.make_url('/login')

    prev_resp = resp.history[0]
    assert prev_resp.status == 302
    assert prev_resp.url == client.make_url('/')


async def test_authorized_user_is_logged_in(aiohttp_client):
    client = await aiohttp_client(create_app())
    make_cookie(client, {'user_id': 1})

    resp = await client.get('/')
    assert resp.status == 200
    assert resp.url == client.make_url('/')
