import requests
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# response = requests.get('https://api.github.com/events')
# config = {
#     'user': os.getenv('DB_USER'),
#     'pass': os.getenv('DB_PASS'),
#     'host': os.getenv('DB_HOST'),
#     'db_name': os.getenv('DB_NAME'),
# }
# 
# engine = create_engine(
#     'postgresql://{user}:{pass}@{host}/{db_name}'.format(**config)
# )
# 
# with engine.connect() as conn:
#     print(conn)
