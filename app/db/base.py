# app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ↓ モデルをサブモジュールごと読み込む（副作用でテーブル登録される）
import app.models