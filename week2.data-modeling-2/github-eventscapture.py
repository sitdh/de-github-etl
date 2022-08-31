from datetime import datetime
from collections import Counter
from dotenv import load_dotenv
load_dotenv()

import database as db
import event as ev
import datetime as dt
import logging

logging.basicConfig(level=logging.DEBUG)

def datetime_convert(datetime_str: str) -> datetime:
    return dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')

def raw_events_reduction(data: list):
    dataset = []
    for d in data:
        element = {k: v for k, v in d.items() if k != 'payload'}

        if 'created_at' in element:
            element['created_at'] = datetime_convert(element['created_at'])

        dataset.append(element)

    return dataset


def main(data: list):
    logging.info('Starting data ingestion')
    dataset = ev.event_reduction(
        data,
        instruction=raw_events_reduction
    )
    logging.info('Sorting data')
    dataset.sort(key=lambda x: x['created_at'], reverse=True)

    # Transactions
    logging.info('Transaction: ingestion')
    transaction_collection = db.get_collection('transactions')
    for data in dataset:
        transaction_collection.update_one(
            {'id': data['id']},
            {'$set': data},
            upsert=True
        )

    logging.info('Transaction: ingestion')

    # Event counter
    logging.info('Events: ingestion')
    event_counter = dict(Counter([t['type'] for t in dataset]))
    events = [{'type': k, 'counter': v} for k, v in event_counter.items()]
    logging.info('Events: Transformed')
    event_collection = db.get_collection('events')
    for event in events:
        event_collection.update_one(
            {'type': event['type']},
            {'$set': event},
            upsert=True
        )
    logging.info('Events: Saved')

    # Actor
    # Transform data with event types counter
    logging.info('Actor: Ingestion')
    actors = {a['actor']['id']: a['actor'] for a in dataset if 'actor' in a}
    for data in dataset:
        if 'actor' not in data:
            continue

        uid = data['actor']['id']

        if data['type'] in actors[uid]:
            actors[uid][data['type']] += 1
        else:
            actors[uid][data['type']] = 1

    logging.info('Actor: Activities categorized by events')

    # save into actors
    actor_collection = db.get_collection('actors')
    for aid, actor in actors.items():
        actor_collection.update_one(
            {'id': aid},
            {'$set': actor},
            upsert=True
        )
    logging.info('Actor: Information saved into database')

    # Repository
    # Transforms to repos with event frequency categorized by type
    repos = {r['repo']['id']: r['repo'] for r in dataset if 'repo' in r}
    logging.info('Repository: Information was categorized by events')
    for data in dataset:
        if 'repo' not in data:
            continue

        rid = data['repo']['id']

        if data['type'] in repos[rid]:
            repos[rid][data['type']] += 1
        else:
            repos[rid][data['type']] = 1

    # Save repo into database
    logging.info('Repository: Saving repo\'s event into collection')
    repo_collection = db.get_collection('repositories')
    for rid, repo in repos.items():
        repo_collection.update_one(
            {'id': rid},
            {'$set': repo},
            upsert=True
        )
    logging.info('Repository: Events saved')

    logging.info('Data ingestion done')


if __name__ == '__main__':
    main(
        data=ev.event_loading('../dataset')
    )