# Url shortener
The base [project](https://github.com/DanTcheche/basic_django_project) used was one created by me.

## Setup

Build project:
- Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/).

- Create a .env file in the root folder (where the manage.py file is) and copy this.
```text
    DATABASE_URL=postgres://development:development@db:5432/development
    DATABASE_TEST_URL=postgres://development:development@localhost/test_db
    DEBUG=True
    
    # CORS
    CORS_ORIGIN_WHITELIST=http://localhost:8080
```

Try next commands with `sudo` if you get permission errors.
- `docker-compose build`.
- `docker-compose up -d`.
- Server will run in port 8000.

### Requirements

This projects requires python 3.6.
Python 3 can be installed with [pyenv](https://github.com/pyenv/pyenv).

1. Use [pyenv-installer](https://github.com/pyenv/pyenv-installer) for installing pyenv
2. See which python versions are available: `pyenv install --list`
3. Install python 3. Example: `pyenv install 3.6.6` (3.6.6 or higher)
4. `pyenv shell 3.6.6`
5. `poetry shell`
6. `poetry install`


### Run test

With the server running and inside the poetry shell after doing the install:
Run  ```py.test``` in the terminal.

### Considerations

- We could add an 'expires' date to the Url model if we want to be able to remove urls from the database after a given time has passed.
That would be desirable if we have millions of users daily.
- If we have a lot of requests maybe it would be better to store short unique urls and use them instead of encoding each time,
that would improve the velocity of the APIs.