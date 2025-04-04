from fastapi import UploadFile, HTTPException
from app.core.whisper_loader import whisper_model
from app.core.config import SENTIMENT_MODEL_JA, SENTIMENT_MODEL_EN
from transformers import pipeline
from app.services.audio_emotion_service import run_smile_analysis, extract_voice_tone_features
from app.core.config import AUDIO_TMP_DIR
import subprocess, shutil, uuid, os, librosa, time, logging

logger = logging.getLogger("uvicorn")
AUDIO_TMP_DIR = "tmp/audio"
os.makedirs(AUDIO_TMP_DIR, exist_ok=True)

# 感情分析モデル取得
def get_sentiment_analyzer(language: str):
    if language == "ja":
        return pipeline("sentiment-analysis", model=SENTIMENT_MODEL_JA, tokenizer=SENTIMENT_MODEL_JA)
    elif language == "en":
        return pipeline("sentiment-analysis", model=SENTIMENT_MODEL_EN)
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")

# テキスト感情からgenkiスコアを推定
def analyze_genki_with_transformers(text: str, analyzer) -> dict:
    result = analyzer(text[:512])[0]
    label = result["label"]
    score = round(result["score"] * 100)

    if label == "POSITIVE":
        genki_score = 80 + int(score / 5)
        comment = "Very energetic"
    elif label == "NEUTRAL":
        genki_score = 50
        comment = "Neutral"
    else:
        genki_score = 30 - int(score / 5)
        comment = "Low energy"

    return {
        "label": label,
        "genki_score": genki_score,
        "judgement": comment,
        "confidence": f"{score}%"
    }

# メイン処理：音声→文字起こし＋感情分析＋トーン分析
async def transcribe_audio(file: UploadFile, language: str, timeout: int):
    """
    Whisper 音声文字起こし＆感情分析API + 声のトーン分析

    - 音声を ffmpeg で変換し、Whisperで解析
    - テキスト感情分析、OpenSMILEで声の分析も追加
    """
    overall_start = time.time()
    input_filename = os.path.join(AUDIO_TMP_DIR, f"input_{uuid.uuid4().hex}_{file.filename}")
    temp_filename = os.path.join(AUDIO_TMP_DIR, f"converted_{uuid.uuid4().hex}.wav")

    with open(input_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        subprocess.run(["ffmpeg", "-y", "-i", input_filename, "-ar", "16000", "-ac", "1", temp_filename],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=400, detail="Failed to convert audio to WAV")

    try:
        y, sr = librosa.load(temp_filename, sr=None)
        duration_sec = librosa.get_duration(y=y, sr=sr)
        if timeout > 0 and duration_sec > timeout:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "録音時間が制限を超えています。" if language == "ja" else "Recording exceeds time limit.",
                    "audio_duration_seconds": round(duration_sec, 2),
                    "allowed_max_seconds": timeout
                }
            )
    except Exception as e:
        logger.error(f"Duration error: {e}")
        raise HTTPException(status_code=400, detail="Invalid or unsupported audio file.")

    try:
        whisper_start = time.time()
        whisper_timed_out = False
        segments = []

        segments_generator, _ = whisper_model.transcribe(temp_filename, language=language)

        for segment in segments_generator:
            if timeout > 0 and (time.time() - whisper_start) > timeout:
                whisper_timed_out = True
                break
            segments.append(segment)

        text = "".join([s.text for s in segments])
        audio_covered = float(segments[-1].end) if segments else 0.0
        cover_rate = round((audio_covered / duration_sec) * 100, 2) if duration_sec > 0 else 0.0
        silence = audio_covered < duration_sec * 0.1
        total_elapsed = round(time.time() - overall_start, 2)

        if whisper_timed_out and not text.strip():
            raise HTTPException(status_code=206, detail="Whisperが音声を検出する前にタイムアウトしました。")

        analyzer = get_sentiment_analyzer(language)
        sentiment = analyze_genki_with_transformers(text, analyzer) if text else {"message": "No speech detected."}

        # OpenSMILEで声のトーン解析
        audio_emotion = {}
        try:
            smile_csv = run_smile_analysis(temp_filename)
            audio_emotion = extract_voice_tone_features(smile_csv)
            os.remove(smile_csv)
        except Exception as e:
            logger.warning(f"OpenSMILE failed: {e}")

        return {
            "transcript": text,
            "sentiment_analysis": sentiment,
            "audio_emotion_analysis": audio_emotion,
            "whisper_analysis": {
                "processed_seconds": round(audio_covered, 2),
                "total_seconds": round(duration_sec, 2),
                "cover_rate_percent": cover_rate,
                "timeout": whisper_timed_out,
                "silence": silence
            },
            "total_processing_time_sec": total_elapsed
        }

    finally:
        for f in [input_filename, temp_filename]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception as cleanup_err:
                logger.warning(f"Cleanup failed: {cleanup_err}")