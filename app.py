import streamlit as st
import time
from chatbot_engine import ChatbotEngine

# --- Setup & Config ---
st.set_page_config(
    page_title="AI Healthcare Assistant",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the blue healthcare theme and modern UI
st.markdown("""
<style>
    :root {
        --primary-blue: #1E88E5;
        --light-blue: #E3F2FD;
        --dark-blue: #0D47A1;
        --text-color: #333333;
    }
    .stApp {
        background-color: #F8FBFF;
    }
    .main-title {
        color: var(--dark-blue);
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-title {
        color: var(--primary-blue);
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    .chat-container {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .user-msg {
        background-color: var(--primary-blue);
        color: white;
        padding: 15px;
        border-radius: 15px 15px 0px 15px;
        margin-bottom: 15px;
        text-align: right;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        max-width: 80%;
        margin-left: auto;
    }
    .bot-msg {
        background-color: white;
        color: var(--text-color);
        padding: 15px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 15px;
        text-align: left;
        border: 1px solid var(--light-blue);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        max-width: 80%;
        margin-right: auto;
    }
    .disclaimer {
        font-size: 0.85rem;
        color: #7f8c8d;
        text-align: center;
        margin-top: 50px;
        padding: 10px;
        border-top: 1px solid #eee;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Initialize Engine ---
@st.cache_resource
def get_engine():
    return ChatbotEngine("symptom_data.csv")

engine = get_engine()

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Healthcare Assistant. How can I help you today?"}
    ]

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100) # Medical icon
    st.title("Navigation")
    
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Healthcare Assistant. How can I help you today?"}
        ]
        st.rerun()
        
    st.markdown("---")
    st.subheader("📌 Quick Links")
    
    def quick_link_action(text):
        st.session_state.messages.append({"role": "user", "content": text})
        with st.spinner("Processing..."):
            time.sleep(0.5)
            response = engine.generate_response(text)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🩺 Symptoms Checker", use_container_width=True):
        quick_link_action("Symptoms Checker")
        st.rerun()
    if st.button("💡 Health Tips", use_container_width=True):
        quick_link_action("Health Tips")
        st.rerun()
    if st.button("🚨 Emergency Protocol", use_container_width=True):
        quick_link_action("Emergency Protocol")
        st.rerun()
    if st.button("📜 Chat History", use_container_width=True):
        quick_link_action("Chat History")
        st.rerun()
    if st.button("ℹ️ About Project", use_container_width=True):
        quick_link_action("About Project")
        st.rerun()
    
    st.markdown("---")
    st.caption("AI Healthcare Chatbot Major Project")
    st.caption("Built with Python & Streamlit")

# --- Main App ---
st.markdown("<h1 class='main-title'>AI Healthcare Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Your personal medical symptom checker</p>", unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        # Determine if it's an emergency/warning message for styling
        icon = "🤖"
        if "🚨" in msg['content']: icon = "🚨"
        elif "⚠️" in msg['content']: icon = "⚠️"
        st.markdown(f"<div class='bot-msg'><b>{icon} AI Assistant:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# Chat Input Area
user_input = st.chat_input("Describe your symptoms here...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-msg'><b>You:</b><br>{user_input}</div>", unsafe_allow_html=True)
    
    # Generate bot response with typing effect simulation
    with st.spinner("Analyzing symptoms..."):
        time.sleep(1) # simulate processing time
        response = engine.generate_response(user_input)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Disclaimer
st.markdown("<div class='disclaimer'>⚠️ <b>DISCLAIMER:</b> This chatbot provides general healthcare information only. It is not a substitute for professional medical advice, diagnosis, or treatment. In case of a medical emergency, please contact your local emergency services immediately.</div>", unsafe_allow_html=True)
