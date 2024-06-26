import logging
from supabase import create_client, Client
from app.config import settings


def logger_factory() -> logging.Logger:
    logger = logging.getLogger("wealthcraft")

    return logger


def supabase_factory() -> Client:
    config = settings.get()

    return create_client(
        config.supabase_url,
        config.supabase_key,
    )


logger = logger_factory()
supabase = supabase_factory()
