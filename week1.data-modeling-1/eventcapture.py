import requests
import sys, getopt, logging
import db

from dotenv import load_dotenv


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

def define_tables(engine):
    from model import Base as bs

    logging.info('Prepare for tables definition')
    for tbl in reversed(bs.metadata.sorted_tables):
        logging.info('Delete table: ' + str(tbl))
        print('Delete table:', str(tbl))
        engine.execute(
            "DROP TABLE IF EXISTS {}".format(
                str(tbl)
            )
        )

    bs.metadata.create_all(engine)

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

    if mode not in ('etl', 'datetime', 'setup'):
        print('githubevent.py -m|--mode=[etl,datetime,etl')
        sys.exit(-2)

    with db.engine.connect() as conn:
        match mode:
            case 'datetime':
                define_tables(db.engine)

            case 'setup':
                pass

            case _:
                pass


if __name__ == '__main__':
    load_dotenv()
    main(sys.argv[1:])