import os

from sqlalchemy import (Column, Integer, MetaData, String, Table, Boolean, create_engine, ARRAY, TEXT)
from databases import Database

from typing import List

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

users = Table(
    'user_info',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50)),
    Column('hashed_password', TEXT),
    Column('email', String(50)),
    Column('full_name', String(50)),
    Column('disabled', Boolean(False)),
    Column('db_connections', ARRAY(String(250)))
)

database = Database(DATABASE_URI)