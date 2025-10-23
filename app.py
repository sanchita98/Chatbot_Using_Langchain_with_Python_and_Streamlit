import streamlit as st
from rag_pipeline import RAGPipeline
from session_manager import SessionManager
from history_manager import HistoryManager
import os

# Streamlit Page Configuration
st.set_page_config(
    page_title="📄 PDF Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  UI Styling
st.markdown("""
<style>
/* Global App Styling */
body {
    background-color: #0f172a; /* deep navy background */
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Streamlit Main Container */
.main {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    padding: 1rem 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.3);
}

/* Title */
h1 {
    text-align: center;
    color: #38bdf8;
    font-size: 2.2rem !important;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(56,189,248,0.3);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(148,163,184,0.15);
}

.sidebar-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #93c5fd;
    margin-bottom: 1rem;
}
 
            
/* Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg, #38bdf8, #3b82f6);
    color: white;
    border: none;
    border-radius: 0.6rem;
    font-weight: 600;
    transition: all 0.3s ease-in-out;
}
button[kind="primary"]:hover {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    transform: scale(1.02);
}

/* File uploader box */
[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.8);
    border: 1px dashed #38bdf8;
    border-radius: 1rem;
    padding: 1rem;
    color: #cbd5e1;
}

/* Chat bubbles */
.stChatMessage {
    padding: 1rem;
    border-radius: 1rem;
    margin: 0.5rem 0;
    line-height: 1.5;
}

.stChatMessage[data-testid="stChatMessage-user"] {
    background: linear-gradient(145deg, #1e3a8a, #3b82f6);
    color: white;
    text-align: right;
    border-top-right-radius: 0;
}

.stChatMessage[data-testid="stChatMessage-assistant"] {
    background: rgba(30, 41, 59, 0.9);
    color: #e2e8f0;
    border-top-left-radius: 0;
}

/* Chat input box */
[data-testid="stChatInputContainer"] {
    background: rgba(15, 23, 42, 0.95);
    border-top: 1px solid rgba(148,163,184,0.2);
    padding-top: 0.5rem;
}
textarea {
    background-color: rgba(30, 41, 59, 0.8);
    color: #e2e8f0 !important;
    border: 1px solid rgba(148,163,184,0.3);
    border-radius: 0.7rem;
}

/* Info boxes */
.stInfo, .stWarning, .stError {
    border-radius: 0.8rem !important;
}

/* Footer */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # stores all session histories

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager(st.session_state.sessions)

if "active_session" not in st.session_state:
    st.session_state.active_session = st.session_state.session_manager.create_session()

if "chat_history" not in st.session_state:
    # link chat_history to the active session
    st.session_state.chat_history = st.session_state.sessions[st.session_state.active_session]

if "last_user_query" not in st.session_state:
    st.session_state.last_user_query = None

# Sidebar
sessions = list(st.session_state.sessions.keys())

# Session selection
if sessions:
    # ✅ Custom large label
    st.sidebar.markdown(
        "<p style='font-size:1.2rem; font-weight:600; color:#93c5fd;'>💬 Select a Conversation:</p>",
        unsafe_allow_html=True
    )

    # Radio with empty label
    selected = st.sidebar.radio(
        "",  # empty label
        sessions,
        index=sessions.index(st.session_state.active_session)
    )

    st.session_state.active_session = selected
    st.session_state.chat_history = st.session_state.sessions[selected]

    # Rename session
    new_name = st.sidebar.text_input("✏️ Rename chat:", value=selected, key=f"rename_input_{selected}")
    if st.sidebar.button("✅ Save Name", use_container_width=True):
        updated_name = st.session_state.session_manager.rename_session(selected, new_name)
        st.session_state.active_session = updated_name
        st.session_state.chat_history = st.session_state.sessions[updated_name]
        st.sidebar.success(f"Renamed to '{updated_name}'")
        st.rerun()
else:
    st.sidebar.write("No saved chats yet.")

# New Chat
if st.sidebar.button("➕ New Chat", use_container_width=True):
    new_session = st.session_state.session_manager.create_session()
    st.session_state.active_session = new_session
    st.session_state.chat_history = st.session_state.sessions[new_session]
    st.rerun()

# Main Title
st.title("🤖 Smart PDF Chatbot")


st.markdown("""
<div style="
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    padding: 0.8rem 1rem;
    border-radius: 0.7rem;
    text-align:center;
    color:#93c5fd;
    font-weight:500;
    margin-bottom:1rem;
">
✨ Ask questions from your PDFs — AI will answer only from your documents.
</div>
""", unsafe_allow_html=True)

st.caption("Upload your knowledge base PDFs and ask questions intelligently.")

# -------------------------------
# File Upload Section
# -------------------------------
uploaded_files = st.file_uploader("📥 Upload PDF files", accept_multiple_files=True, type="pdf")

if uploaded_files:
    pdf_paths = []
    os.makedirs("data", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(file_path)

    # Initialize persistent pipeline and history manager
    if "pipeline" not in st.session_state or st.session_state.pipeline is None:
        st.session_state.pipeline = RAGPipeline(st.session_state.active_session, pdf_paths)
        st.session_state.history_manager = HistoryManager(st.session_state.active_session)
        # Load existing history for the active session
        st.session_state.chat_history = st.session_state.history_manager.load_history()

    pipeline = st.session_state.pipeline
    history_manager = st.session_state.history_manager

    # -------------------------------
    # Display Previous Chat
    # -------------------------------
    if len(st.session_state.chat_history) == 0:
        st.markdown("<p style='text-align:center; color:gray;'>💬 Start chatting with your PDFs!</p>", unsafe_allow_html=True)
    else:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat Input
    user_query = st.chat_input("💭 Ask a question about your PDFs...")

    if user_query:
        # Avoid duplicate processing on rerun
        if user_query != st.session_state.get("last_user_query", None):
            st.session_state.last_user_query = user_query

            with st.chat_message("user"):
                st.markdown(user_query)

            answer = pipeline.ask(user_query)

            with st.chat_message("assistant"):
                st.markdown(answer)

            # Save to history manager
            history_manager.save_turn("user", user_query)
            history_manager.save_turn("assistant", answer)

            # Update session-specific chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.session_state.sessions[st.session_state.active_session] = st.session_state.chat_history

            # 🧠 Auto-rename session based on first question
            if "Untitled Chat" in st.session_state.active_session or st.session_state.active_session.startswith("session_"):
                suggested_name = user_query.split(" ")[0].capitalize() + " Chat"
                new_name = st.session_state.session_manager.rename_session(
                    st.session_state.active_session, suggested_name
                )
                st.session_state.active_session = new_name
                st.session_state.chat_history = st.session_state.sessions[new_name]
        else:
            st.stop()
else:
    st.info("📘 Upload your PDFs to start chatting. Your session will be saved automatically.")
