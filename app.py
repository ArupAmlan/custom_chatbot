import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = st.secrets["HF_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    print("DEBUG RAW:", response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"{response.status_code} - {response.text}"}

st.title("🤖 Arup ChatBot")

if "history" not in st.session_state:
    st.session_state.history = []

for u, b in st.session_state.history:
    st.chat_message("user").write(u)
    st.chat_message("assistant").write(b)

user_input = st.chat_input("Ask anything...")

if user_input:
    st.chat_message("user").write(user_input)

    prompt = f"<s>[INST] {user_input} [/INST]"
    output = query({"inputs": prompt})

    try:
        full_reply = output[0]["generated_text"]
        # Remove prompt part
        bot_reply = full_reply.split("[/INST]")[-1].strip()
    except Exception:
        bot_reply = output.get("error", "⚠️ Unexpected error.")

    st.chat_message("assistant").write(bot_reply)
    st.session_state.history.append((user_input, bot_reply))
