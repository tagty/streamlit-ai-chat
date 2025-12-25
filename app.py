import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# ページ設定
st.set_page_config(page_title="AI Chat", page_icon="💬")
st.title("💬 AI Chat Assistant")

# LLM の初期化
@st.cache_resource
def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )

llm = get_llm()

# システムプロンプト
SYSTEM_PROMPT = "あなたは親切で知識豊富な日本語の技術アシスタントです。ユーザーの質問に対して、わかりやすく丁寧に回答してください。"

# session_state の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 会話履歴を表示
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# ユーザー入力
if prompt := st.chat_input("メッセージを入力してください"):
    # ユーザーメッセージを表示・保存
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # AI の応答を生成
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            # システムプロンプト + 会話履歴を含めて送信
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + st.session_state.messages
            response = llm.invoke(messages)
            st.markdown(response.content)

    # AI メッセージを保存
    st.session_state.messages.append(AIMessage(content=response.content))
