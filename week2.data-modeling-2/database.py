import pymongo as mg
import os

client = None

def connection_string():
    return 'mongodb://{u}:{p}@{h}:27017/'.format(
        u=os.getenv('DB_USERNAME', 'user'),
        p=os.getenv('DB_PASSWORD', 'password'),
        h=os.getenv('DB_HOST', 'host_name'),
    )

def db_client(conn_str: str = None):
    global client

    if client == None:
        con_string = connection_string() if None == conn_str else conn_str
        client = mg.MongoClient(
            con_string,
            serverSelectionTimeoutMS=5_000
        )

    return client

def get_collection(collection: str):
    global client

    client = db_client() if client == None else client

    return client[os.getenv('DB_NAME')][collection]