# Github Event ETL

## Project Preparation

1. Database (Postgres + PGAdmin)
```
$ docker compose up
```

2. Install dependencies by `venv`  
```
$ python3 -m vevn venv && souce venv/bin/activate
$ pip install -r requirements.txt
```

In case of error raised while installing psycopg2 on macOS, it can fix by run command  
```
$ brew postgresql-upgrade-database
```

Then, run command above again.
