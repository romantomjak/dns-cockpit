from functools import wraps

from aiohttp import web
from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_security import authorized_userid


class DatabaseAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, app):
        self.app = app

    async def authorized_userid(self, identity):
        async with self.app['db'].acquire() as conn:
            stmt = await conn.prepare("SELECT COUNT(*) FROM `users` WHERE `email` = $1 AND `is_active` = true")
            ret = await stmt.fetchval(identity)
            if ret:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        return False  # nothing allowed for now :o


def login_required(fn):
    @wraps(fn)
    async def wrapped(*args, **kwargs):
        request = args[-1]
        if not isinstance(request, web.BaseRequest):
            msg = ("Incorrect decorator usage. "
                   "Expecting `def handler(request)` "
                   "or `def handler(self, request)`.")
            raise RuntimeError(msg)

        userid = await authorized_userid(request)
        if userid is None:
            raise web.HTTPFound('/login')

        ret = await fn(*args, **kwargs)
        return ret

    return wrapped
