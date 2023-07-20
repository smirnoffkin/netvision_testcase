# Netvision test task

#### P.S. A detailed description of the task can be found in [netwision-testcase.md](./netwision-testcase.md). ####

## Run
### Production

1. `make env`
2. `make up-prod`
3. `make up-client`

### Development

1. `make env`
2. `make dev`
3. `make up-dev`
4. `make migrate`
5. `make run`
6. `make up-client`

Go to `http://localhost:8080/docs` to see open api docs

## Project technology stack

* Python (FastAPI, asyncio, SQLAlchemy, pytest, alembic), PostgreSQL, Redis, Docker
