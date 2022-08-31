from dotenv import load_dotenv
load_dotenv()

import os
import pymongo as mg

cont_str = 'mongodb://{u}:{p}@{h}:27017/'.format(
    u=os.getenv('DB_ROOT_USERNAME', 'user'),
    p=os.getenv('DB_ROOT_PASSWORD', 'password'),
    h=os.getenv('DB_HOST', 'host_name'),
)

client = mg.MongoClient(
    cont_str,
    serverSelectionTimeoutMS=5_000
)

db = client['data']

user = db['users']
user_id = user.insert_one({
    'user': 'johnd',
    'text': 'hello',
}).inserted_id

print(user_id)