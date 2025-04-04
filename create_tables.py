# create_tables.py

import asyncio
from app.db.session import engine
from app.db.base import Base  # モデルが登録されているBase

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ テーブル作成が完了しました")

if __name__ == "__main__":
    asyncio.run(init_models())