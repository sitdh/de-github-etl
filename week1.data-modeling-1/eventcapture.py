import requests
import sys, getopt, logging
import db

from dotenv import load_dotenv

from model import Base


# response = requests.get('https://api.github.com/events')

def define_tables(engine):
    from model import Base as bs

    logging.info('Prepare for tables definition')
    bs.metadata.drop_all(engine)

    logging.info('Create tables')
    print('Create tables')
    bs.metadata.create_all(engine)
    logging.info('All table created')
    print('All table created')

def main(argv):
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

    if mode not in ('etl', 'datetime', 'setup', 'all'):
        print(__file__, '-m|--mode=[setup,datetime,etl,all]')
        sys.exit(-2)

    with db.engine.connect() as conn:
        match mode:
            case 'datetime':
                # define_tables(db.engine)
                pass

            case 'setup':
                define_tables(db.engine)

            case 'all':
                define_tables(db.engine)

            case _:
                pass

if __name__ == '__main__':
    load_dotenv()
    main(sys.argv[1:])
