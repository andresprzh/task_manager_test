"""Shared SQLAlchemy plumbing for every per-feature repository module.

Holds the single declarative ``Base`` that all ORM classes register on, plus
the engine/sessionmaker setup. It deliberately imports no ORM module of its
own: the feature modules import *this*, never the other way around. See the
package ``__init__`` for how the tables get registered before ``create_all``.
"""

import asyncio

from sqlalchemy import Column, Enum
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DEFAULT_DB_URL = "sqlite+aiosqlite:///./task_manager.db"


def enum_column(enum_cls, default):
    """Persist an enum by its lowercase value rather than its member name."""
    return Column(
        Enum(enum_cls, values_callable=lambda e: [member.value for member in e]),
        default=default,
        nullable=False,
    )


async def init_async_db(db_url: str = DEFAULT_DB_URL) -> sessionmaker:
    """Initialize the database and return an async sessionmaker."""
    engine = create_async_engine(db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return maker


def init_db_sync(db_url: str = DEFAULT_DB_URL) -> sessionmaker:
    # helper for synchronous startup code
    return asyncio.run(init_async_db(db_url))
