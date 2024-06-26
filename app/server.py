from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import game, auth, turn
from app.config import settings
from app.models import create_all_tables


def app_factory() -> FastAPI:
    config = settings.get()
    meta = config.metadata()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        create_all_tables()

        yield

    app = FastAPI(
        title=meta["name"],
        version=meta["version"],
        summary=meta["summary"],
        description=meta["description"],
        lifespan=lifespan,
        redoc_url="/docs",
        docs_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(game.router)
    app.include_router(auth.router)
    app.include_router(turn.router)

    return app


app = app_factory()
