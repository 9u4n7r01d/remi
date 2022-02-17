from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from remi.core.constant import Client


async def dispose_all_engines():
    await async_engine.dispose()


async_engine = create_async_engine(f"sqlite+aiosqlite:///{Client.config_path}/config.sqlite", future=True)

async_sql_session = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=True,
)
