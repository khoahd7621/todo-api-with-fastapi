# Python Web Develop with FastAPI Assignment

A FastAPI sample application to learn how to use FastAPI with SQLAlchemy and PostGreSQL.

# Sample Setup

## Prepare environment

At root folder, do the following stuffs

- Create a virtual environment using `virtualenv` module in python.

```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```

- Start postgres docker container (You can change the configuration in `docker-compose.yml` file)

```bash
docker compose up -d
```

- At `app` directory, create `.env` file by creating a copy from `.env.sample`, remember to update `DEFAULT_PASSWORD` and `JWT_SECRET` variables

## Migrate data

- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible.

```bash
# Migrate to latest revison
alembic upgrade head
```

## Start application

- At `app` directory, run `uvicorn` web server (`reload` mode is for development purposes)

```bash
uvicorn main:app --reload
```

- Access `http://localhost:8000/docs` and start exploring APIs
