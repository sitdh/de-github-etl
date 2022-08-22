import os, requests, json
from re import I

from model import Event

class EventReader(object):
    def read(self) -> list:
        raise NotImplementedError('Not Implement yet')

class EventStaticFileReader(EventReader):
    def __init__(self, path: str):
        self._path = path

    def read(self) -> list:
        if not os.path.isdir(self._path):
            raise FileNotFoundError(f'File not found: {self._path}')

        json_files = [f"{self._path}/{file}" for file in os.listdir(self._path) \
            if file[-4:] == 'json']

        dataset = []
        for json_file in json_files:
            with open(json_file) as f:
                dataset += json.load(f)

        return dataset

class EventAPIReader(EventReader):
    def __init__(self):
        self._event_api = 'https://api.github.com/events'

    def read(self) -> list:
        response = requests.get(self._event_api)
        if response.status_code not in (200, 201):
            raise ConnectionError('Connection failure')

        return response.json()

class EventAdapter:
    
    def __init__(self):
        self._adapters = []

    def addAdapters(self, adapter: list):
        self._adapters += adapter

    def clearAdapter(self):
        self._adapters = []

    def read(self) -> list:
        dataset = []

        for reader in self._adapters:
            dataset += reader.read()

        return dataset

class EventParser:
    def __init__(self):
        pass

    def parse(self, message):
        public_status = 1 if message.get('public') else 0
        date_id = 0

        # prepare for actor
        actor_id = 0 # save and get actor id
        org_id = 0 # save and get org id
        repo_id = 0 # save and get repo id
        date_id = 0 # save and get date id

        return {
            'event_id': message.get('event_id'),
            'event_type': message.get('type'),
            'actor_id': actor_id, # message.get('actor', {'id': None}).get('id'),
            'repo_id': repo_id, # message.get('repo', {'id': None}).get('id'),
            'org_id': org_id, # message.get('org', {'id', None}).get('id'),
            'payload': str(message.get('payload')),
            'created_at': str(message.get('created_at')),
            'public': public_status,
            'date_id': date_id,
        }
 
            
if __name__ == '__main__':
    adapter = EventAdapter()

    adapter.addAdapters([
        EventStaticFileReader('./dataset'),
        EventAPIReader()
    ])

    parser = EventParser()

    for event in adapter.read():
        print(parser.parse(event))
        break