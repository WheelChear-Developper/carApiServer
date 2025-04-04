# app/crud/user.py

from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.hash import bcrypt
import uuid

# ユーザー重複チェック（username または email）
async def get_user_by_username_or_email(db, username: str, email: str):
    result = await db.execute(
        select(User).where((User.username == username) | (User.email == email))
    )
    return result.scalar_one_or_none()

# 新規ユーザー登録（ハッシュ化＋APIキー生成）
async def create_user(db, user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    api_key = uuid.uuid4().hex

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        api_key=api_key
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user