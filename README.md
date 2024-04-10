# NHS Innovation Service Homepage
NHS Innovation Service Homepage is the entry point of all NHS services related to innovations.

It is built with **Wagtail**, an open source content management framework.

This README describes how to set up and run the project, but there are other docs (e.g. about search) in the [docs folder](./docs)

## Requirements

- Docker and docker-dompose

The whole wagtail environment runs on docker. All the libraries are setup on the container.

## Configuration
This project is prepared to run locally with Wagtail, PostgreSQL DB and Elastic Search served through Docker and Docker compose. Run the following intructions inside the project folder.

## Running locally
### 1. Start local Wagtail, Postgres DB and Elastic Search servers through docker and docker compose
```bash
$ docker-compose -f ./docker-compose.yml up &
```

### 2. Relevant Wagtail commands
Configure wagtail superuser:
``` bash
$ docker exec <wagtail-container-id> "python3 manage.py createsuperuser"
```

Re-index Elastic Search:
``` bash
$ docker exec <wagtail-container-id> "python3 manage.py update_index"
```

To collect the static files (only when they change):
``` bash
$ docker exec <wagtail-container-id> "$ python3 manage.py collectstatic --clear --noinput && python3 manage.py comprress"
```

### 3. Postgres DB Seeding

It's important that the seeding is done before running the containers.
Two seed files are require:
- `./.db-seed/0.sql` to create some required roles. 
- `./.db-seed/1.sql` to restore the DB.

To dump the DB from the Dev, proper permissions to access are required.
Consult with the DevOps for permissions and proper credentials.

To create the dump:
``` bash
# NOTE: the pg_dump version should be the same as the DB
PGPASSWORD=<INFORMATIONAL-PG-SQL-PASSWORD> \
pg_dump --file "1.sql" \
  --host "<PGHOST>" \
  --port "5432" \
  --username "<INFORMATIONAL-PG-SQL-USER>" \
  --no-password \
  --verbose \
  --no-privileges \
  "is_homepage"
```

## Running in production
To run in production mode update .env file with:
```bash
DJANGO_SETTINGS_MODULE=is_homepage.settings.production
ALLOWED_HOSTS={YOUR_HOSTS_HERE}
```
You may need to rebuild the wagtail container.
