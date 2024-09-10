# NHS Innovation Service Homepage
NHS Innovation Service Homepage is the entry point of all NHS services related to innovations.

It is built with **Wagtail**, an open source content management framework.

This README describes how to set up and run the project, but there are other docs (e.g. about search) in the [docs folder](./docs)

## Requirements
- Python
- Pip
- Docker and Docker compose

The following installation instructions are for any linux ubuntu flavored environment:

``` bash
# Install needed OS packages.
$ sudo apt-get install python3 python3-pip libpq-dev gettext pango1.0-tools


# Install docker + docker compose.
## Install system packages
$ sudo apt-get update
$ sudo apt-get install gnupg ca-certificates

## Install GPG keys:
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg

## Add the repository to APT sources:
$ echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt-get update

## Install packages.
$ sudo apt-get install docker-ce docker-ce-cli docker-compose
$ sudo usermod -a -G docker $USER


# Install PIP global packages.
$ pip install pipenv # Install virtual environments
```

## Configuration
This project is prepared to run locally using a virtual environment for the runtime, and additionally layers (PostgreSQL DB and Elastic Search) served through Docker and Docker compose. Run the following intructions inside the project folder.

### 1. Configure environment variables
Make a copy of the file ".env.example", and call it ".env" changing any variable as needed.

### 2. Start local DB server through docker and docker compose
```bash
$ docker-compose -f .docker/docker-compose.yml up
```

### 3. Configure your virtual environment
``` bash
$ pipenv shell # This will create your new virtual environment, where everything runs.
$ pip install -r requirements.txt # Install dependencies
$ wagtail updatemodulepaths # Update dependencies with changes in module paths. This will be needed until all dependencies are updated to the wagtail version used. (https://docs.wagtail.org/en/stable/releases/3.0.html#changes-to-module-paths)
$ python3 manage.py migrate # Run migrations.
$ python3 manage.py createsuperuser # Create admin user to access your local admin area.

```
Everything will be installed and ready to run from the virtual environment.


## Running locally
### 1. Start local DB server through docker and docker compose.
```bash
$ docker-compose -f .docker/docker-compose.yml up
```
### 2. Make sure that you are inside your virtual environment. If not, execute the command:
```bash
$ pipenv shell
```
To exit from the virtual environment, type `$ deactivate`
### 3. Run the app
```bash
$ python3 manage.py runserver
```

## Running in production mode
To run in production mode update .env file with:
```bash
DJANGO_SETTINGS_MODULE=is_homepage.settings.production
ALLOWED_HOSTS={YOUR_HOSTS_HERE}
```

You also need to collect the static files by running the following command (only need to do this when the static files change):
```bash
$ python3 manage.py collectstatic --clear --noinput
$ python3 manage.py compress
```


















# To review

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
$ docker exec <wagtail-container-id> "python3 manage.py collectstatic --clear --noinput && python3 manage.py comprress"
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

### 4. Wagtail Assets

Download the assets from Azure: [download.zip](https://nhse-innovation-service-informational-dev.scm.azurewebsites.net/api/zip/media/)
Copy the following folders to `.wagtail-media`:
```
- documents
- images
- original_images
```


## Running in production
To run in production mode update .env file with:
```bash
DJANGO_SETTINGS_MODULE=is_homepage.settings.production
ALLOWED_HOSTS={YOUR_HOSTS_HERE}
BASEURL={BASEURL}
```
You may need to rebuild the wagtail container.
