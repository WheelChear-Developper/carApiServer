# app/db/session.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./users.db")

# エンジン作成（async）
engine = create_async_engine(DATABASE_URL, echo=False)

# セッションファクトリ
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 依存関係として使用（FastAPIのDependsで利用）
async def get_db():
    async with SessionLocal() as session:
        yield session