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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --primary: #2563EB;
        --primary-gradient: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        --bot-bg: #FFFFFF;
        --bg-color: #F8FAFC;
        --text-main: #0F172A;
        --text-muted: #64748B;
        --border-color: #E2E8F0;
        --sidebar-bg: #FDF2F8; /* Soft pink background for the sidebar */
    }
    
    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* Main Headers */
    .main-title {
        text-align: center;
        font-weight: 800;
        font-size: 3rem;
        letter-spacing: -0.03em;
        margin-bottom: 5px;
        background: -webkit-linear-gradient(45deg, #1E293B, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title {
        color: var(--text-muted);
        text-align: center;
        font-size: 1.15rem;
        font-weight: 500;
        margin-bottom: 40px;
    }
    
    /* Chat Messages Container */
    .user-msg {
        background: var(--primary-gradient);
        color: white;
        padding: 16px 22px;
        border-radius: 20px 20px 4px 20px;
        margin-bottom: 18px;
        text-align: left;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3), 0 8px 10px -6px rgba(37, 99, 235, 0.1);
        max-width: 75%;
        margin-left: auto;
        font-size: 1.05rem;
        line-height: 1.5;
        animation: fadeIn 0.3s ease-in-out;
    }
    .bot-msg {
        background-color: var(--bot-bg);
        color: var(--text-main);
        padding: 16px 22px;
        border-radius: 20px 20px 20px 4px;
        margin-bottom: 18px;
        text-align: left;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        max-width: 80%;
        margin-right: auto;
        font-size: 1.05rem;
        line-height: 1.6;
        animation: fadeIn 0.4s ease-in-out;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Disclaimer */
    .disclaimer {
        font-size: 0.85rem;
        color: #991B1B;
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Styling Overrides */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }
    
    /* Modern Streamlit Buttons */
    div[data-testid="stButton"] > button {
        border-radius: 12px;
        border: 1px solid var(--border-color);
        background-color: white;
        color: var(--text-main);
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    div[data-testid="stButton"] > button:hover {
        border-color: var(--primary);
        color: var(--primary);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1), 0 4px 6px -4px rgba(37, 99, 235, 0.1);
        transform: translateY(-2px);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
