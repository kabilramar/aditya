import streamlit as st
import os
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="DSA Bot: Divide & Conquer", page_icon="🧠", layout="centered")
st.title("🧠 Divide & Conquer Chatbot")
st.caption("Master recursion, Merge Sort, Quick Sort, and Binary Search with relatable examples.")

# 2. API Key Setup (Updated for Render)
# Check OS environment variables first (Render), then fallback to Streamlit secrets (Local)
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("Please add your GEMINI_API_KEY to Render Environment Variables or `.streamlit/secrets.toml`")
        st.stop()

# 3. Model Configuration & Connection Management
system_instruction = (
    "You are an expert Data Structures and Algorithms instructor. "
    "Your focus is exclusively on the 'Divide and Conquer' paradigm. "
    "You are teaching engineering students from rural areas. "
    "When explaining algorithms like Merge Sort, Quick Sort, or Binary Search, "
    "always use relatable local examples—such as organizing village festival logistics, "
    "managing crop yields, analyzing rainfall data, or local sports like Jallikattu—to "
    "make technical recursion concepts intuitive. "
    "Break down problems clearly into: 1. Divide, 2. Conquer, 3. Combine."
)

@st.cache_resource
def get_chat_session():
    # Pass the extracted api_key here
    client = genai.Client(api_key=api_key)
    
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": system_instruction
        }
    )
    return client, chat

client, chat = get_chat_session()

# 4. Initialize Chat History in Streamlit UI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I can help you master Divide & Conquer algorithms. Want to start with a real-world example of Binary Search?"}
    ]

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Handle User Input
if prompt := st.chat_input("Ask about an algorithm (e.g., Merge Sort)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            response = chat.send_message_stream(prompt)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error communicating with Gemini API: {e}")
