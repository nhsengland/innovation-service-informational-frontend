# NHS Innovation Service Homepage
NHS Innovation Service Homepage is the entry point of all NHS services related to innovations.

It is built with **Wagtail**, an open source content management framework.


## Requirements
- Python
- Pip
- Docker and Docker compose

The following installation instructions are for any linux ubuntu flavored environment:

``` bash
# Install python and Pip
$ sudo apt-get install python3
$ sudo apt-get install python3-pip

# Install docker + docker compose 
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu RELEASE stable" # Check RELEASE in "cat /etc/os-release", UBUNTU_CODENAME
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli docker-compose

$ sudo usermod -a -G docker $USER # Optional command, if errors about permissions happens when running commands

# Install global packages.
$ pip install pipenv # Install virtual environments
$ pip install autopep8 # Install code formatter.
```
---

## Configuration
This project is prepared to run locally using a virtual environment for the runtime, and additionally layers (PostgreSQL DB) served through Docker and Docker compose. Run the following intructions inside the project folder.

### 1. Configure environment variables
Make a copy of the file ".env.example", and call it ".env"

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
$ python3 manage.py createsuperuser # Create admin user to access yout local admin area.

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

## Running in production
To run in production mode update .env file with:
```bash
DJANGO_SETTINGS_MODULE=is_homepage.settings.production
ALLOWED_HOSTS={YOUR_HOSTS_HERE}
```

You also need to collect the static files by running the following command (only need to do this when the static files change):
```bash
$ python3 manage.py collectstatic --clear --noinput
$ python3 manage.py comprress
```
