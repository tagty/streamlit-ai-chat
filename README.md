# AI Chat Assistant

Streamlit + LangChain を使った ChatGPT 風の AI チャットアプリ

## 特徴

- ChatGPT 風のモダンな UI
- 会話履歴を考慮した自然な対話
- 日本語での技術アシスタント
- シンプルな単一ファイル構成

## 技術スタック

- **Python 3.10+**
- **Streamlit**: チャット UI フレームワーク
- **LangChain**: LLM 統合フレームワーク
- **OpenAI API**: gpt-4o-mini モデル（temperature: 0.7）

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd streamlit-ai-chat
```

### 2. 仮想環境の作成と有効化

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env` ファイルを作成して、OpenAI API キーを設定してください。

```bash
cp .env.example .env
```

`.env` ファイルを編集:
```
OPENAI_API_KEY=sk-...
```

OpenAI API キーは [こちら](https://platform.openai.com/api-keys) から取得できます。

### 5. アプリの起動

```bash
streamlit run app.py
```

ブラウザで http://localhost:8501 が自動的に開きます。

## 使い方

1. チャット入力欄にメッセージを入力
2. Enter キーまたは送信ボタンで送信
3. AI が会話履歴を考慮して日本語で返答します
4. 会話は session_state に保存され、ページをリロードするまで保持されます

## プロジェクト構成

```
streamlit-ai-chat/
├── app.py              # メインアプリケーション（全機能を含む）
├── requirements.txt    # Python 依存パッケージ
├── .env.example       # 環境変数のテンプレート
├── .env               # 環境変数（git 管理外）
├── .gitignore         # Git 除外設定
├── README.md          # このファイル
└── CLAUDE.md          # Claude Code 用ガイド
```

## カスタマイズ

### モデルの変更

`app.py` の 17 行目でモデルを変更できます：

```python
model="gpt-4o-mini",  # gpt-4o, gpt-4-turbo など
```

### システムプロンプトの変更

`app.py` の 24 行目でシステムプロンプトを変更できます：

```python
SYSTEM_PROMPT = "あなたのカスタムプロンプト"
```

### Temperature の調整

`app.py` の 18 行目で温度パラメータを調整できます（0.0〜2.0）：

```python
temperature=0.7,  # 低いほど決定的、高いほど創造的
```

## ライセンス

MIT
