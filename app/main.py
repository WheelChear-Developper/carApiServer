from fastapi import FastAPI
from app.api import transcribe, greeting, user

app = FastAPI()

# 各APIのルーターを追加
app.include_router(transcribe.router)
app.include_router(greeting.router)
app.include_router(user.router)