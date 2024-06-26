# Ethyca Technical Challenge

## How to run:

You can run this project both by using the docker-compose file or by running everything locally with uvicorn, celery (the redis instance needs docker) and supabase cli.


Install the application:
```bash
poetry install
poetry shell
```

Run the task queue for celery:
```bash
docker compose up -d redis
```

Run the worker:
```bash
poetry run celery -A app.worker worker
```

Run the server:
```bash
app serve
```

## Total time spent on this project

4 hours and 23 minutes (non-continuous).
I used a lot of recycled code from this projects I built in the past to speed up the development and infrastructure:
- [gilgates-api](https://github.com/Z33DD/gilgates-api)
- [wealthcraft-api](https://github.com/Z33DD/wealthcraft-api)

## Assumptions:
- There are always only two players
- Player 1 always get X and player 2 alwayes get O
- As I'm using Supabase, the frontend can have realtime access to changes made in the database.
- No game will be abandoned
- Performance matters
  
## Tradeoffs
I build a very specific way to interact with the database with the DAO I created, so it will need to be heavly updated as the codebase evolves. Also, the way this in heavly typed can be hard for developer that don't understand Python typing hunts.

## Unique features:
- Realtime changes with Supabase
- Asynchronous requests using an ASGI server
- Background task using celery
- Good test coverage
- SQLite db for testing and PostgreSQL for production
- Scalability between poducers and cosumers of the task queue
  
## My feedback
I would like to have more time to improve the application because I think it is a bit messy as I used code from different projects to build this one.
