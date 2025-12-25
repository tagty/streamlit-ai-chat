# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Streamlit + LangChain で構築された ChatGPT 風 AI チャットアプリ。OpenAI の gpt-4o-mini モデルを使用し、日本語での会話をサポート。シンプルさを重視した単一ファイル構成。

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

**LLM の初期化** (app.py:14-21)
- `@st.cache_resource` で ChatOpenAI インスタンスをキャッシュ
- gpt-4o-mini、temperature 0.7 で設定
- `python-dotenv` で環境変数を読み込み

**状態管理** (app.py:26-28)
- 会話履歴は `st.session_state.messages` に保存
- LangChain のメッセージ型を使用：`HumanMessage`, `AIMessage`, `SystemMessage`
- システムプロンプトは session_state に保存せず、毎回 API 呼び出し時に付与

**メッセージフロー** (app.py:37-52)
1. `st.chat_input()` でユーザー入力を取得
2. ユーザーメッセージを表示し session_state に追加
3. システムプロンプト + 会話履歴全体を LLM に送信
4. AI の応答を表示し session_state に追加

### 重要なパターン

**システムプロンプトの扱い**
- API 呼び出しごとに会話履歴の先頭に追加（47行目）
- session_state に保存しないことで、状態リセットなしで変更可能

**メッセージタイプの判定**
- `isinstance(message, HumanMessage)` でロールを判定（32行目）
- UI のチャットバブルのスタイリングに使用

## 設定

- **モデル**: gpt-4o-mini (app.py:17)
- **Temperature**: 0.7 (app.py:18)
- **システムプロンプト**: 日本語の技術アシスタント (app.py:24)
- **ページ設定**: タイトル "AI Chat"、アイコン 💬 (app.py:10)
