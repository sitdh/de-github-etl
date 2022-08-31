from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

import database as db
import event as ev
import datetime as dt

def datetime_convert(datetime_str: str) -> datetime:
    return dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')

def raw_events_reduction(data: list):
    dataset = []
    for d in data:
        element = {k: v for k, v in d.items() if k != 'payload'}
        element['event_id'] = element['id']
        del element['id']

        if 'created_at' in element:
            element['created_at'] = datetime_convert(element['created_at'])

        dataset.append(element)

    return dataset

dataset = ev.event_reduction(
    ev.event_loading('../dataset'),
    instruction=raw_events_reduction
)

dataset.sort(key=lambda x: x['created_at'], reverse=True)

transaction = db.get_collection('transactions')
transaction.insert_many(dataset)