import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from remi.core.constant import Client


async def dispose_all_engines():
    await async_config_engine.dispose()


ASYNC_ENGINE_SCHEMA = f"sqlite+aiosqlite:///{Client.DATA_PATH}"


def create_engine(db_filename: str) -> tuple[sqlalchemy.ext.asyncio.AsyncEngine, sqlalchemy.orm.sessionmaker]:
    async_engine = create_async_engine(f"{ASYNC_ENGINE_SCHEMA}/{db_filename}", future=True)
    async_session_maker = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=True,
    )
    return async_engine, async_session_maker


async_config_engine, async_config_session = create_engine("config.sqlite")
