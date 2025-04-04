import subprocess
import pandas as pd
import os
import uuid

# OpenSMILEを実行して音声特徴量をCSV出力
def run_smile_analysis(wav_path: str, config_path: str = "app/services/smile_config/emobase.conf") -> str:
    output_csv = f"/tmp/smile_output_{uuid.uuid4().hex}.csv"
    try:
        subprocess.run([
            "SMILExtract",
            "-C", config_path,
            "-I", wav_path,
            "-O", output_csv
        ], check=True)
        return output_csv
    except Exception as e:
        raise RuntimeError(f"OpenSMILE execution failed: {e}")

# CSVからピッチ・エネルギーを抽出し、genki_scoreを算出
def extract_voice_tone_features(csv_path: str) -> dict:
    df = pd.read_csv(csv_path, sep=';')
    if df.empty:
        return {}

    row = df.iloc[-1]  # 最後の行に特徴量
    pitch = float(row.get('F0final_sma', 0.0))
    energy = float(row.get('pcm_RMSenergy_sma', 0.0))

    genki_score = min(100, int(pitch * 0.1 + energy * 50))
    judgement = "元気そうな声です" if genki_score >= 70 else "落ち着いた声です"

    return {
        "pitch": round(pitch, 2),
        "energy": round(energy, 2),
        "genki_score": genki_score,
        "judgement": judgement
    }