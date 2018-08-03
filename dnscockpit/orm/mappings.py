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
    return metadata
