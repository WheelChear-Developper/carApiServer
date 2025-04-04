from fastapi import APIRouter, Query
from app.services.greeting_service import generate_greeting_set

router = APIRouter()

@router.get("/greeting-set/")
async def greeting_api(name: str = Query(...), language: str = Query("ja")):
    """
    挨拶メッセージ生成API（朝・昼・晩の体調気遣いメッセージ）

    指定された名前と言語（ja/en）に応じて、朝・昼・晩の挨拶をランダムに生成します。
    挨拶文には「体調を気遣う」ニュアンスが含まれており、親しみやすい文面です。

    機能:
    - 毎回異なるランダムな挨拶メッセージを返却
    - 日本語・英語どちらにも対応
    - フォーマルな文面とカジュアルな文面を含む

    パラメータ:
    - name: 相手の名前（例：まさと）
    - language: 挨拶の言語（'ja' または 'en'）

    レスポンス例（language=ja）:
    {
      "morning": "まさとさん、おはようございます。体調はどうですか？",
      "afternoon": "こんにちは、まさとさん。お身体に無理はしていませんか？",
      "evening": "まさとさん、今日の疲れは残っていませんか？"
    }

    レスポンス例（language=en）:
    {
      "morning": "Good morning, Masato. How are you feeling today?",
      "afternoon": "Hi Masato, how’s your energy this afternoon?",
      "evening": "Good evening, Masato. Did you feel okay throughout the day?"
    }

    HTTPレスポンスコード:
    - 200: 正常にメッセージを返却
    - 400: languageが'ja'または'en'以外の場合
    """
    return generate_greeting_set(name, language)
