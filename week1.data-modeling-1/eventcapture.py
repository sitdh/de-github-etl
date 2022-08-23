from calendar import month
from cgi import print_environ
import sys, getopt, logging, os
import db
import datetime as dt

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import select
from event import EventAdapter, EventFulfillment, EventParser
from model import Event
from tqdm.auto import tqdm

logging.basicConfig(level=logging.DEBUG)

def read_event_static(engine):
    """
    Reading github event from json files and github api
    by EventAdapter with JSON reader and API reader => withDefaultReader().
    Then fill missing value with EventFulFillment
    """
    adapter = EventAdapter.withDefaultReader()
    parser = EventParser()
    fulfillment = EventFulfillment(engine)

    events = []
    for e in tqdm(adapter.read(), desc='Loading data from datasouce'):
        events.append((
            parser.parse(e),
            e
        ))

    with Session(engine) as s:
        for event, e in tqdm(events, desc='Ingest data into db'):
            stm = select(Event).where(Event.event_id==event.get('event_id'))
            result = s.execute(stm).fetchone()
            if None == result:
                s.add(
                    fulfillment.fill((event, e))
                )

        s.commit()

def _prepare_datetime(date, timediff):
    """
    Pre-calculated datetime with timediff
    """
    from model import Datetime

    _date = date + dt.timedelta(seconds=timediff)

    """
    Extract date parts to store in DB
    """
    return Datetime(
        id=int(_date.timestamp()),
        the_datetime=_date,
        the_datetime_str=str(_date),
        the_date=_date.date(),
        the_day=_date.day,
        the_month=_date.month,
        the_year=_date.year,
        the_time=_date.time(),
        the_hour=_date.hour,
        the_minute=_date.minute,
        the_second=_date.second
    )

def prepare_datetime(engine):
    """
    Pre-calculated date and time 
    """
    import datetime as dt

    from sqlalchemy.orm import Session

    batch_size = 10_000

    current_datetime = dt.datetime.now()
    after_datetime = current_datetime + dt.timedelta(
        days=int(os.getenv('DAYS_AFTER', '10'))
    )
    before_datetime = current_datetime + dt.timedelta(
        days=int(os.getenv('DAYS_BEFORE', '10')) * (-1)
    )

    print(after_datetime, before_datetime)
    seconds = int((after_datetime - before_datetime).total_seconds())
    pbar = tqdm(total=seconds)

    with Session(engine) as s:
        for i in range(0, seconds, batch_size):
            dates = []
            for j in range(i, min(i+batch_size, seconds)):
                dates.append(
                    _prepare_datetime(current_datetime, j)
                )
                pbar.update(1)

            s.bulk_save_objects(dates)
            del dates

            s.commit()

def define_tables(engine):
    """
    Drop all existing tables (If it exists), then define it.
    """
    from model import Base as bs

    logging.info('Prepare for tables definition')
    bs.metadata.drop_all(engine)

    logging.info('Create tables')
    print('Remove exists tables')

    bs.metadata.create_all(engine)

    logging.info('All table created')
    print('Create tables')

def main(argv):
    """
    Main function to execute command with user's actions

    - setup: Define tables in schema. In case of table already exists, script will drop tables from schema.
    - datetime: Pre-calculated date and time but optional
    - etl: Load git events from json file (example file) and github's api into database
    - all: Do all steps above

    """
    try:
        opts, args = getopt.getopt(
            argv, "m:", ['mode=']
        )
    except:
        sys.exit(-1)
    
    mode = 'etl' # 'datetime' | 'etl
    for opt, arg in opts:
        if opt in ('-m', '--mode'):
            mode = arg.lower()

    mode = 'all' if None == mode else mode.lower()

    if mode not in ('etl', 'datetime', 'all', 'setup',):
        print(__file__, '-m|--mode=[setup,datetime,etl,all]')
        sys.exit(-2)

    match mode:
        case 'datetime':
            prepare_datetime(db.engine)

        case 'setup':
            define_tables(db.engine)

        case 'etl':
            read_event_static(db.engine)

        case 'all':
            print('Redefine tables')
            define_tables(db.engine)

            print('Prepare datetime')
            prepare_datetime(db.engine)

            print('Reading and load to DB')
            read_event_static(db.engine)

if __name__ == '__main__':
    load_dotenv()
    main(sys.argv[1:])
