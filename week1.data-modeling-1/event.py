import os, requests, json, logging
import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session
from re import I

from model import Datetime, Event, Organize, Repository, User

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
            'date': [],
        }

    @property
    def engine(self):
        return self._engine

    def __actor(self, info):
        uid = info.get('id')

        if uid in self._local_cache['actor'].keys():
            u = self._local_cache['actor'][uid]
        else:
            with Session(self.engine) as s:
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
                else:
                    u = m[0].id

                self._local_cache['actor'][uid] = u

        return u

    def __repo(self, info):
        rid = info.get('id')

        if rid in self._local_cache['repo']:
            r = self._local_cache['repo'][rid]
        else:
            stm = select(Repository).where(Repository.repo_id == rid)
            with Session(self.engine) as s:
                rp = s.execute(stm).fetchone()
                if None == rp:
                    repo = Repository(
                        repo_id=info.get('id'),
                        name=info.get('login'),
                        url=info.get('url'),
                    )

                    s.add(repo)
                    s.commit()

                    r = repo.id
                else:
                    r = rp[0].id

                self._local_cache['repo'][rid] = r

        return r

    def __org(self, info):
        oid = info.get('id')

        if oid in self._local_cache['org']:
            r = self._local_cache['org'][oid]
        else:
            stm = select(Organize).where(Organize.org_id == oid)
            with Session(self.engine) as s:
                og = s.execute(stm).fetchone()
                if None == og:
                    org = Organize(
                        org_id=info.get('id'),
                        login=info.get('login'),
                        gravatar_id=info.get('gravatar_id'),
                        url=info.get('url'),
                        avatar_url=info.get('avatar_url'),
                    )

                    s.add(org)
                    s.commit()

                    r = org.id
                else:
                    r = og[0].id

                self._local_cache['org'][oid] = r

        return r

    def __date(self, info):
        d = dt.datetime.strptime(info, '%Y-%m-%dT%H:%M:%SZ')
        ts = int(d.timestamp())

        if ts not in self._local_cache['date']:
            _datetime = Datetime(
                id=ts,
                the_datetime=d,
                the_datetime_str=str(d),
                the_date=d.date(),
                the_day=d.day,
                the_month=d.month,
                the_year=d.year,
                the_time=d.time(),
                the_hour=d.hour,
                the_minute=d.minute,
                the_second=d.second
            )

            with Session(self.engine) as s:
                try:
                    s.add(_datetime)
                    s.commit()
                except:
                    logging.debug(f'Row {ts} already exists')

        return ts

    def fill(self, event_data) -> Event:
        event, message = event_data

        # actor id
        event['actor_id'] = self.__actor(message.get('actor'))

        # repo id
        event['repo_id'] = self.__repo(message.get('repo'))

        # org id
        event['org_id'] = self.__org(message.get('org'))

        # date id
        event['date_id'] = self.__date(message.get('created_at'))

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