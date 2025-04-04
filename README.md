# 📘 Care API Server - プロジェクト概要

## 🔰 このプロジェクトについて
Care API Server は、音声からの体調把握やメンタル分析を目的とした API システムです。主に以下の機能を提供します：

- Whisper を使用した音声文字起こし
- Transformers による感情分析（テキスト）
- OpenSMILE による声のトーン分析（音響特徴量）
- 朝昼晩の体調を気遣う挨拶メッセージ生成
- ユーザー登録・APIキー発行・認証制御

## 📁 ディレクトリ構成

```
careApiServer/
├── app/
│   ├── api/                  # エンドポイント定義
│   │   ├── transcribe.py     # /transcribe API
│   │   ├── greeting.py       # /greeting-set API
│   │   └── user.py           # /register など
│   ├── core/                # 設定や外部モデルの読み込み
│   │   ├── config.py
│   │   └── whisper_loader.py
│   ├── crud/                # DB操作ロジック
│   │   └── user.py
│   ├── db/                  # DB接続とBase
│   │   ├── session.py
│   │   └── base.py
│   ├── models/              # SQLAlchemyモデル
│   │   └── user.py
│   ├── schemas/             # Pydanticスキーマ
│   │   └── user.py
│   └── services/            # ビジネスロジック
│       ├── whisper_service.py
│       └── audio_emotion_service.py
├── smile_config/            # OpenSMILE の設定ファイル（emobase.conf など）
├── .env                     # 環境変数（モデル設定やDB URLなど）
├── requirements.txt         # 必要なパッケージ一覧
└── main.py                  # FastAPI アプリ起動点
```

## ⚙️ 機能一覧

### 🔊 /transcribe
音声ファイルを元に：
- Whisper で文字起こし
- Transformers で感情分析（テキスト）
- OpenSMILE で音響特徴から元気度推定

### 💬 /greeting-set
- 名前と言語を元に、体調を気遣う挨拶を返却

### 👤 /register
- ユーザー登録（username, email, password）
- APIキー自動発行
- 重複チェックとハッシュ保存対応

## 🛠 使用技術
- Python 3.12
- FastAPI
- SQLAlchemy + SQLite（他DBも可）
- transformers（感情分析）
- faster-whisper
- OpenSMILE（音響特徴分析）
- dotenv

## 🚀 実行手順
```bash
# 仮想環境の作成と起動
python -m venv whisper-env
source whisper-env/bin/activate

# パッケージのインストール
pip install -r requirements.txt

# サーバー起動
uvicorn app.main:app --reload
```

## 📝 .env サンプル
```
WHISPER_MODEL_SIZE=medium
WHISPER_DEVICE=cpu
SENTIMENT_MODEL_JA=koheiduck/bert-japanese-finetuned-sentiment
SENTIMENT_MODEL_EN=distilbert-base-uncased-finetuned-sst-2-english
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

---

## 🔒 補足（今後）
- APIキーによるリクエスト認証
- ユーザーごとの利用制限
- フロント連携・ダッシュボード連携

---

Created by: @developper

