import logging

from sqlalchemy import (
    create_engine,
    Table, Column, Integer, String, DateTime, Boolean
)
from sqlalchemy.schema import MetaData


class SQLAlchemy:

    def __init__(self, dsn):
        engine = create_engine(dsn)
        self._metadata = MetaData(engine)

    def create_all_tables(self):
        logging.debug("Creating all DB tables")
        self._metadata.create_all()

    def configure_mappings(self):
        logging.debug("Configuring DB mappings")
        user = Table('users', self._metadata,
            Column('id', Integer, primary_key=True),
            Column('email', String(254), nullable=False),  # compliant with RFCs 3696 and 5321
            Column('password', String(128), nullable=False),
            Column('last_login', DateTime()),
            Column('created_at', DateTime()),
            Column('is_active', Boolean()),
        )
        sessions = Table('sessions', self._metadata,
            Column('id', String(40), primary_key=True),
            Column('data', String(262144), nullable=False),  # approx. 1 mb
            Column('expires_at', DateTime(), nullable=False),
        )
        return self._metadata
