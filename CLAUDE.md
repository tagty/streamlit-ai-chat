# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Streamlit + LangChain で構築された ChatGPT 風 AI チャットアプリ。複数の OpenAI モデルを選択可能で、日本語での会話をサポート。シンプルさを重視した単一ファイル構成。

## 開発環境のセットアップ

### 環境構築
```bash
# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# .env ファイルに OpenAI API キーを設定
OPENAI_API_KEY=sk-...
```

### アプリの起動
```bash
# 仮想環境を有効化してから実行
source venv/bin/activate

# Streamlit アプリを起動（ブラウザで http://localhost:8501 が開く）
streamlit run app.py
```

## アーキテクチャ

### 単一ファイル設計
全機能を `app.py` 1ファイルに集約。初学者でも理解しやすいシンプルな構成を採用。

### 主要コンポーネント

**モデル料金定義** (app.py:10-15)
- `MODEL_PRICING` 辞書で各モデルの input/output 料金（$/1M tokens）を管理

**LLM の初期化** (app.py:22-27)
- `@st.cache_resource` で ChatOpenAI インスタンスをキャッシュ
- model と temperature を引数に取り、組み合わせごとにキャッシュ
- `python-dotenv` で環境変数を読み込み

**サイドバー** (app.py:33-45)
- モデル選択セレクトボックス：gpt-4o-mini / gpt-4o / gpt-4.1 / gpt-4.1-mini
- Temperature スライダー：0.0〜2.0（デフォルト 0.7）
- Clear Conversation ボタン：会話履歴とコストをリセット
- Cost 表示：セッション累積コストを `$0.000000` 形式で表示

**状態管理** (app.py:49-53)
- 会話履歴は `st.session_state.messages` に保存
- 累積コストは `st.session_state.total_cost` に保存
- LangChain のメッセージ型を使用：`HumanMessage`, `AIMessage`, `SystemMessage`
- システムプロンプトは session_state に保存せず、毎回 API 呼び出し時に付与

**メッセージフロー** (app.py:62-79)
1. `st.chat_input()` でユーザー入力を取得
2. ユーザーメッセージを表示し session_state に追加
3. システムプロンプト + 会話履歴全体を LLM に送信
4. AI の応答を表示し session_state に追加
5. `response.response_metadata.token_usage` からトークン数を取得してコスト計算・累積

### 重要なパターン

**システムプロンプトの扱い**
- API 呼び出しごとに会話履歴の先頭に追加
- session_state に保存しないことで、状態リセットなしで変更可能

**メッセージタイプの判定**
- `isinstance(message, HumanMessage)` でロールを判定
- UI のチャットバブルのスタイリングに使用

**コスト計算**
- `(prompt_tokens * input_price + completion_tokens * output_price) / 1_000_000` で計算
- セッション中の累積コストを `st.session_state.total_cost` で管理

## 設定

- **モデル**: サイドバーで選択（デフォルト: gpt-4o-mini）(app.py:35-39)
- **Temperature**: サイドバーのスライダーで設定（デフォルト: 0.7）(app.py:40)
- **システムプロンプト**: 日本語の技術アシスタント (app.py:30)
- **ページ設定**: タイトル "AI Chat"、アイコン 💬 (app.py:18)
