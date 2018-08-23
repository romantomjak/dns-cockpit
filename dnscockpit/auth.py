from functools import wraps

import inject
from aiohttp import web
from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_session import get_session


class DatabaseAuthorizationPolicy(AbstractAuthorizationPolicy):
    db = inject.attr('db')

    async def authorized_userid(self, identity):
        async with self.db as conn:
            stmt = await conn.prepare("SELECT * FROM `users` WHERE `email` = $1 AND `is_active` = true")
            ret = await stmt.fetchval(identity)
            if ret:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True


def login_required(fn):
    @wraps(fn)
    async def wrapped(*args, **kwargs):
        request = args[-1]
        session = await get_session(request)
        router = request.app.router
        if 'user_id' not in session:
            return web.HTTPFound(router['login'].url_for())
        ret = await fn(*args, **kwargs)
        return ret

    return wrapped
