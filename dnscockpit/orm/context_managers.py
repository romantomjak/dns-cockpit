import logging


class ConnectionManager:

    def __init__(self, pool):
        self.pool = pool

    async def __aenter__(self):
        logging.debug("Acquiring DB connection")
        self.connection = await self.pool.acquire()
        return self.connection

    async def __aexit__(self, exc_type, exc_value, traceback):
        logging.debug("Releasing DB connection")
        await self.pool.release(self.connection)
        self.connection = None


class TransactionManager:

    def __init__(self, connection):
        self.connection = connection

    async def __aenter__(self):
        logging.debug("Entering transaction")
        self.was_committed_or_rolled_back = False
        self.session = self.connection.transaction()
        await self.session.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logging.debug("Exiting transaction")
        if not self.was_committed_or_rolled_back:
            logging.info("No explicit commit or rollback detected, rolling back")
            self.rollback()
        self.session = None

    def commit(self):
        logging.debug("Committing transaction")
        self.was_committed_or_rolled_back = True
        self.session.commit()

    def rollback(self):
        logging.debug("Rolling back transaction")
        self.was_committed_or_rolled_back = True
        self.session.rollback()
