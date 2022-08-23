import os, requests, json
from sqlalchemy import select
from sqlalchemy.orm import Session
from re import I

from model import Event, User

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

    @classmethod
    def withDefaultReader(cls):
        adapter = EventAdapter()
        adapter.addAdapters([
            EventStaticFileReader('./dataset'),
            EventAPIReader()
        ])

        return adapter

    def read(self) -> list:
        dataset = []

        for reader in self._adapters:
            dataset += reader.read()

        return dataset

class EventParser:

    def parse(self, message) -> dict:
        public_status = 1 if message.get('public') else 0

        return {
            'event_id': message.get('event_id'),
            'event_type': message.get('type'),
            'actor_id': message.get('actor', {'id': None}).get('id'),
            'repo_id': message.get('repo', {'id': None}).get('id'),
            'org_id': message.get('org', {'id', None}).get('id'),
            'payload': str(message.get('payload')),
            'created_at': str(message.get('created_at')),
            'public': public_status,
        }

class EventFulfillment:
    def __init__(self, engine):
        self._engine = engine
        self._local_cache = {
            'repo': {},
            'actor': {},
            'org': {},
        }

    def __actor(self, info):
        uid = info.get('id')

        print(info)

        if uid in self._local_cache['actor']:
            u = self._local_cache['actor'][uid]
            print('exits')
        else:
            with Session(self._engine) as s:
                stm = select(User).where(
                    User.user_id == info.get('id')
                )

                m = s.execute(stm).fetchone()
                if None == m:
                    user = User(
                        user_id=info.get('id'),
                        login=info.get('login'),
                        display_login=info.get('display_login'),
                        gravatar_id=info.get('gravatar_id'),
                        url=info.get('url'),
                        avatar_id=info.get('avatar_id'),
                    )

                    s.add(user)
                    s.commit()

                    u = user.id
                    print('xxxxx')
                else:
                    u = m[0].id
                    print('cache')

                self._local_cache['actor'][uid] = u

        return u
                

    def __repo(self, info):
        pass

    def __org(self, info):
        pass

    def __date(self, info):
        pass

    def fill(self, event_data) -> Event:
        event, message = event_data

        # actor id
        event['actor_id'] = self.__actor(message.get('actor'))

        # repo id
        event['repo_id'] = self.__repo(message.get('repo'))

        # org id
        event['org_id'] = self.__repo(message.get('org'))

        # date id
        event['date_id'] = self.__repo(message.get('created_at'))

        return Event(**event)
 
            
if __name__ == '__main__':
    adapter = EventAdapter()

    adapter.addAdapters([
        EventStaticFileReader('./dataset'),
        EventAPIReader()
    ])

    parser = EventParser()

    events = []
    for e in adapter.read():
        events.append((
            parser.parse(e), 
            e
        ))

    print(events)