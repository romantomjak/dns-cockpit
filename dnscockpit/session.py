import uuid
from datetime import datetime, timedelta

import inject
from aiohttp_session import AbstractStorage, Session


class PostgreSQLStorage(AbstractStorage):
    db = inject.attr('db')

    async def load_session(self, request):
        cookie = self.load_cookie(request)
        if cookie is None:
            return Session(None, data=None, new=True, max_age=self.max_age)
        else:
            async with self.db as conn:
                key = str(cookie)
                stmt = await conn.prepare("SELECT data FROM sessions WHERE id = $1 AND expires_at > $2")
                data = await stmt.fetchval(key, datetime.utcnow())
                if data is None:
                    return Session(None, data=None, new=True, max_age=self.max_age)
                try:
                    data = self._decoder(data)
                except ValueError:
                    data = None
                return Session(key, data=data, new=False, max_age=self.max_age)

    async def save_session(self, request, response, session):
        key = session.identity
        if key is None:
            key = uuid.uuid4().hex
            self.save_cookie(response, key, max_age=session.max_age)
        else:
            if session.empty:
                self.save_cookie(response, '', max_age=session.max_age)
            else:
                self.save_cookie(response, key, max_age=session.max_age)

        data = self._encoder(self._get_session_data(session))
        async with self.db as conn:
            async with conn.transaction():
                max_age = session.max_age
                expire = max_age if max_age is not None else datetime.utcnow() + timedelta(hours=1)  # 1h by default
                if session.new:
                    stmt = await conn.prepare("INSERT INTO sessions (id, data, expires_at) VALUES ($1, $2, $3)")
                else:
                    stmt = await conn.prepare("UPDATE sessions SET data=$2, expires_at=$3 WHERE id=$1")
                await stmt.fetchval(key, data, expire)
