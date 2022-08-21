import os, sys

from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

_dbconfig = {
    'user': os.getenv('DB_USER'),
    'pass': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'name': os.getenv('DB_NAME'),
}

engine = create_engine(
    'postgresql://{user}:{pass}@{host}/{name}'.format(
        **_dbconfig
    )
)