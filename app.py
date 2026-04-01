import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# モデルごとの料金 ($/1M tokens)
MODEL_PRICING = {
    "gpt-4o-mini":  {"input": 0.15,  "output": 0.60},
    "gpt-4o":       {"input": 2.50,  "output": 10.00},
    "gpt-4.1":      {"input": 2.00,  "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40,  "output": 1.60},
}

# ページ設定
st.set_page_config(page_title="AI Chat", page_icon="💬")
st.title("💬 AI Chat Assistant")

# LLM の初期化
@st.cache_resource
def get_llm(model: str, temperature: float):
    return ChatOpenAI(
        model=model,
        temperature=temperature
    )

# システムプロンプト
SYSTEM_PROMPT = "あなたは親切で知識豊富な日本語の技術アシスタントです。ユーザーの質問に対して、わかりやすく丁寧に回答してください。"

# サイドバー
with st.sidebar:
    st.title("Options")
    selected_model = st.selectbox(
        "Choose a model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1", "gpt-4.1-mini"]
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.total_cost = 0.0
        st.rerun()
    st.divider()
    total_cost = st.session_state.get("total_cost", 0.0)
    st.metric("Cost", f"${total_cost:.6f}")

llm = get_llm(selected_model, temperature)

# session_state の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0

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

    # コストを計算して累積
    usage = response.response_metadata.get("token_usage", {})
    pricing = MODEL_PRICING.get(selected_model, {"input": 0, "output": 0})
    cost = (usage.get("prompt_tokens", 0) * pricing["input"] + usage.get("completion_tokens", 0) * pricing["output"]) / 1_000_000
    st.session_state.total_cost += cost

    # AI メッセージを保存
    st.session_state.messages.append(AIMessage(content=response.content))
