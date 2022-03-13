from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from remi.core.constant import Client


async def dispose_all_engines():
    await async_config_engine.dispose()


async_engine_scheme = f"sqlite+aiosqlite:///{Client.config_path}"

async_config_engine = create_async_engine(f"{async_engine_scheme}/config.sqlite", future=True)
async_config_session = sessionmaker(
    async_config_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=True,
)
