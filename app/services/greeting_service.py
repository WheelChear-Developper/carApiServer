from fastapi import HTTPException
import random

def generate_greeting_set(name: str, language: str):
    """
    挨拶メッセージ生成API（体調を気遣う朝・昼・晩の挨拶）

    指定された名前・言語（ja/en）に基づいて体調を聞く挨拶メッセージをランダムに生成します。
    """
    greetings = {
        "ja": {
            "morning": [
                f"おはよう、{name}さん。今日の体調はいかがですか？",
                f"{name}さん、おはようございます。お変わりないですか？",
                f"おはようございます、{name}さん。体調に問題はないですか？",
            ],
            "afternoon": [
                f"こんにちは、{name}さん。お昼ですが体調は大丈夫ですか？",
                f"{name}さん、こんにちは。無理しすぎていませんか？",
                f"こんにちは、{name}さん。体調の変化などありませんか？",
            ],
            "evening": [
                f"こんばんは、{name}さん。一日の疲れは大丈夫ですか？",
                f"{name}さん、こんばんは。今日の体調はどうでしたか？",
                f"こんばんは、{name}さん。夜になりましたが、体調はお変わりないですか？",
            ]
        },
        "en": {
            "morning": [
                f"Good morning, {name}. How are you feeling today?",
                f"Morning, {name}. Did you sleep well?",
                f"Hi {name}, how's your condition this morning?"
            ],
            "afternoon": [
                f"Good afternoon, {name}. How are you doing today?",
                f"Hi {name}, feeling okay this afternoon?",
                f"Hello {name}, is your body doing alright so far today?"
            ],
            "evening": [
                f"Good evening, {name}. How was your day?",
                f"Hi {name}, how are you feeling tonight?",
                f"Evening, {name}. Any discomfort today?"
            ]
        }
    }

    if language not in greetings:
        raise HTTPException(status_code=400, detail="Unsupported language")

    return {
        "morning": random.choice(greetings[language]["morning"]),
        "afternoon": random.choice(greetings[language]["afternoon"]),
        "evening": random.choice(greetings[language]["evening"]),
    }
