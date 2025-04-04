from faster_whisper import WhisperModel
from app.core.config import WHISPER_MODEL_SIZE, WHISPER_DEVICE

whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type="int8")