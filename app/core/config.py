import os
from dotenv import load_dotenv

load_dotenv()

WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "medium")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
SENTIMENT_MODEL_JA = os.getenv("SENTIMENT_MODEL_JA", "koheiduck/bert-japanese-finetuned-sentiment")
SENTIMENT_MODEL_EN = os.getenv("SENTIMENT_MODEL_EN", "distilbert-base-uncased-finetuned-sst-2-english")
AUDIO_TMP_DIR = os.getenv("AUDIO_TMP_DIR", "tmp/audio")
os.makedirs(AUDIO_TMP_DIR, exist_ok=True)