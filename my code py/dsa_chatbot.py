import streamlit as st
from google import genai

# --- Page config ---
st.set_page_config(page_title="DSA Chatbot", page_icon="📚")
st.title("📚 DSA & SQL Tutor Chatbot")

# --- Load knowledge base ---
@st.cache_resource
def load_kb():
    with open("DSA CHATBOT.txt", "r") as f:
        return f.read()

kb = load_kb()

# --- System prompt ---
SYSTEM_PROMPT = f"""
You are a polite, encouraging, and highly organized academic tutor chatbot designed to help students learn Data Structures and Algorithms (DSA) and SQL. 

You will be provided with reference content from a text document. Your primary rule is to answer the student's questions using ONLY the information provided in that reference text. 

When formatting your responses, you must strictly follow these rules:
1. Always start with a polite and encouraging greeting.
2. Break down the explanation into a clean, logical sequence (step-by-step).
3. Use bullet points or numbered lists for every key concept to make it easy to read and digest.
4. Keep explanations clear and beginner-friendly.
5. If the student asks a question that cannot be answered using the provided text, politely inform them that you do not have that information in your current study materials.

{kb}
"""

# --- Initialize chat in session state (avoids closed client issue) ---
if "chat" not in st.session_state:
    # PASTE YOUR API KEY HERE
    client = genai.Client(api_key="AIzaSyAlAPr_SXU94ZJeGcFllRKbNz68xijD2zs")
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User input ---
if user_input := st.chat_input("Ask me about DSA or SQL..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(user_input)
            reply = response.text
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
