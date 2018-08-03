from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean


def configure_mappings(metadata):
    user = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('email', String(254), nullable=False),  # compliant with RFCs 3696 and 5321
        Column('password', String(128), nullable=False),
        Column('last_login', DateTime()),
        Column('created_at', DateTime()),
        Column('is_active', Boolean()),
    )
    sessions = Table('sessions', metadata,
        Column('id', String(40), primary_key=True),
        Column('data', String(262144), nullable=False),  # approx. 1 mb
        Column('expires_at', DateTime(), nullable=False),
    )
    return metadata
