from fastapi import APIRouter, UploadFile, File, Query
from app.services.whisper_service import transcribe_audio

router = APIRouter()

@router.post("/transcribe/")
async def transcribe_api(
    file: UploadFile = File(...),
    language: str = Query("ja"),
    timeout: int = Query(20)
):
    """
    Whisper 音声文字起こし・感情分析・声のトーン分析API

    このエンドポイントは、音声ファイルに対して以下の解析を実行します：

    ① Whisper による文字起こし
    - アップロードされた音声（.m4a, .mp3等）を .wav に変換
    - Whisper モデルで指定言語（ja/en）に応じた文字起こし
    - timeout（秒）を超えた場合は中断し、部分結果を返却

    ② 感情分析（transformersを利用）
    - テキストからポジティブ/ネガティブなどの感情を分類
    - スコアに基づいて「genki_score（元気度）」と判断コメントを生成

    ③ 声のトーン分析（OpenSMILEを利用）
    - 音声のピッチやエネルギーから、声の元気度を推定
    - 結果として別の genki_score を出力し、声の印象を評価

    ④ その他の情報
    - 処理時間、カバー率、無音判定、Whisperのタイムアウト状況などを返却

    レスポンス例:
    {
      "transcript": "...",
      "sentiment_analysis": {
        "label": "POSITIVE",
        "genki_score": 90,
        "judgement": "Very energetic",
        "confidence": "85%"
      },
      "audio_emotion_analysis": {
        "pitch": 170.3,
        "energy": 0.83,
        "genki_score": 78,
        "judgement": "元気そうな声です"
      },
      "whisper_analysis": {
        "processed_seconds": 15.2,
        "total_seconds": 20.5,
        "cover_rate_percent": 74.1,
        "timeout": false,
        "silence": false
      },
      "total_processing_time_sec": 18.4
    }

    パラメータ:
    - file: 音声ファイル（必須）
    - language: 文字起こしと感情分析の言語（ja or en）
    - timeout: Whisper の最大処理時間（秒）。0 で無制限

    HTTPレスポンスコード:
    - 200: 正常に解析終了
    - 206: Whisper タイムアウトで一部結果のみ返却
    - 400: ファイルエラー・変換失敗など
    - 422: 録音時間が timeout を超過
    - 500: 内部エラー（WhisperやOpenSMILEの失敗など）
    """
    return await transcribe_audio(file, language, timeout)
