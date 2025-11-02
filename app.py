import streamlit as st
from rag_pipeline import RAGPipeline
from session_manager import SessionManager
from history_manager import HistoryManager
import os

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(
    page_title="📄 AskMyDocs AI", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 🎨 Modern UI Styling: Desert Bloom (Light Mode)
# -------------------------------
st.markdown("""
<style>
/* ===== Global Base Styling ===== */
body {
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease-in-out;
}

/* ===== Default (Light Mode - Desert Bloom) ===== */
body {
    background-color: #FFF9BD; /* Very Pale Cream/Ivory */
    color: #1a202c; /* Dark text */
}

/* ===== Main Container/Page Wrapper ===== */
.main {
    background: #ffffff;
    padding: 1.5rem 2.5rem;
    border-radius: 1.2rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05); 
}

/* ===== Title & Header ===== */
h1 {
    text-align: center;
    color: #A3DC9A !important; /* Soft Mint Green */
    font-size: 2.5rem !important;
    font-weight: 800;
    text-shadow: 0 0 5px rgba(163, 220, 154, 0.3);
    margin-bottom: 0.5rem;
}

/* ===== Sidebar Styling ===== */
[data-testid="stSidebar"] {
    background: #DEE791; /* Pale Chartreuse/Creamy Green Sidebar */
    border-right: 1px solid #A3DC9A;
}
.sidebar-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #D1A980; /* Muted Sand/Tan */
    margin-bottom: 1rem;
}

/* Ensure radio buttons text is clear in light mode */
.stRadio > label > div[data-testid="stMarkdownContainer"] p {
    color: #1a202c !important;
    font-weight: 500;
}


/* ===== Buttons (Primary - Soft Peach Accent) ===== */
button[kind="primary"] {
    /* Soft Peach/Terracotta Gradient for high contrast accent */
    background: linear-gradient(90deg, #FFD6BA, #FFBC99); /* Peach to Lighter Peach */
    color: #4b4b4b; /* Dark text for contrast */
    border: none;
    border-radius: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 0.6rem 1rem;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}
button[kind="primary"]:hover {
    background: linear-gradient(90deg, #FFC7A5, #FFB28C);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(255, 214, 186, 0.6);
}

/* ===== File Uploader Area ===== */
[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 2px dashed #A3DC9A; /* Soft Mint Green dashed border */
    border-radius: 1.2rem;
    padding: 1.5rem;
    color: #1a202c;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ===== Chat Messages: General Style (Note: Streamlit chat elements are difficult to position with pure CSS) ===== */
.stChatMessage {
    padding: 1rem 1.2rem;
    border-radius: 1.2rem;
    margin: 0.7rem 0;
    line-height: 1.6;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    /* Remove default alignment to allow column layout to work */
    width: fit-content; 
    max-width: 70%; 
}

/* --- Specific Bubble Styles for Look & Feel (Alignment controlled by Python) --- */

/* User Chat Message (Sand/Tan Bubble) - Will be placed on the LEFT using columns */
.stChatMessage[data-testid="stChatMessage-user"] {
    background: #D1A980; /* Muted Sand/Tan */
    color: #ffffff;
    /* Removed text-align: right to center text in the LEFT column bubble */
    border-bottom-right-radius: 1.2rem; 
    border-top-left-radius: 0.4rem;
    font-weight: 500;
}

/* Assistant Chat Message (Clean White/Cream) - Will be placed on the RIGHT using columns */
.stChatMessage[data-testid="stChatMessage-assistant"] {
    background: #FFF9BD; /* Pale Cream */
    color: #1a202c;
    border: 1px solid #DEE791;
    /* Added text-align: right to look better in the RIGHT column bubble */
    text-align: left; 
    border-bottom-left-radius: 1.2rem; 
    border-top-right-radius: 0.4rem;
}

/* ===== Chat Input Container ===== */
[data-testid="stChatInputContainer"] {
    background: #FFF9BD;
    border-top: 1px solid #A3DC9A;
    padding-top: 1rem;
}
textarea {
    background-color: #ffffff;
    color: #1a202c !important;
    border: 1px solid #DEE791;
    border-radius: 1rem;
    padding: 0.8rem;
}

/* ===== Info/Alert Boxes (Subtle Green) ===== */
.stInfo {
    border-radius: 1rem !important;
    background-color: #E6F3E6 !important; 
    color: #558B2F !important; 
    border: 1px solid #A3DC9A;
}

/* ===== Custom Header Box (Green/Cream adapted) ===== */
.custom-header-box {
    background: #DEE791; /* Creamy Green wash */
    border: 1px solid #A3DC9A;
    padding: 1rem 1.5rem;
    border-radius: 1rem;
    text-align:center;
    color:#D1A980;
    font-weight:600;
    font-size: 1.1rem;
    margin-bottom:1.5rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

/* ===== Custom Footer Style ===== */
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #ffffff; 
    color: #94a3b8; 
    text-align: center;
    padding: 0.5rem 0;
    font-size: 0.75rem;
    border-top: 1px solid #e0e0e0;
    z-index: 1000;
}

/* ===== Footer (Hide default Streamlit footer) ===== */
footer {
    visibility: hidden;
}

/* Dark mode fallback (for comprehensive style block) */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: #f7f7f7;
    }
    .main {
        background: #2a2a2a;
    }
    h1 {
        color: #A3DC9A !important;
    }
    .footer {
        background-color: #2a2a2a;
        color: #b0b0b0;
        border-top: 1px solid #4d4d4d;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# Initialize Session State (LOGIC PRESERVED)
# -------------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager(st.session_state.sessions)

if "active_session" not in st.session_state:
    st.session_state.active_session = st.session_state.session_manager.create_session()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = st.session_state.sessions[st.session_state.active_session]

if "last_user_query" not in st.session_state:
    st.session_state.last_user_query = None

# -------------------------------
# Sidebar: Chat Sessions and Controls
# -------------------------------
sessions = list(st.session_state.sessions.keys())

# --- New Chat Button ---
if st.sidebar.button("🚀 Start New Document Dive", use_container_width=True, help="Start a fresh conversation and upload new documents."):
    new_session = st.session_state.session_manager.create_session()
    st.session_state.active_session = new_session
    st.session_state.chat_history = st.session_state.sessions[new_session]
    st.session_state.pipeline = None 
    st.session_state.history_manager = None
    st.rerun() 

st.sidebar.markdown("---")


# --- Session Selection ---
st.sidebar.markdown(
    "<p class='sidebar-title' style='color:#D1A980;'>🧭 Active Explorations:</p>",
    unsafe_allow_html=True
)
if sessions:
    selected = st.sidebar.radio(
        "",  # empty label
        sessions,
        index=sessions.index(st.session_state.active_session)
    )

    if selected != st.session_state.active_session:
        st.session_state.active_session = selected
        st.session_state.chat_history = st.session_state.sessions[selected]
        st.session_state.pipeline = None
        st.session_state.history_manager = None
        st.rerun()

    # --- Rename session ---
    st.sidebar.markdown("---")
    
    current_session_name = st.session_state.active_session
    new_name = st.sidebar.text_input("🖋️ Refine Title:", value=current_session_name, key=f"rename_input_{current_session_name}")
    
    if st.sidebar.button("⭐ Save / Rename Title", use_container_width=True, key="save_rename_btn"):
        if new_name and new_name != current_session_name:
            updated_name = st.session_state.session_manager.rename_session(current_session_name, new_name)
            st.session_state.active_session = updated_name
            st.session_state.chat_history = st.session_state.sessions[updated_name]
            st.sidebar.success(f"Renamed to '{updated_name}'")
            st.rerun()
        elif new_name == current_session_name:
            st.sidebar.warning("Title is unchanged.")

else:
    st.sidebar.info("Start a new chat to see your conversation history here.")


# -------------------------------
# Main Title & Welcome
# -------------------------------
st.title("📄 AskMyDocs AI: Your Document Companion") 


st.markdown("""
<div class="custom-header-box">
📄 **Knowledge Navigator:** Ask questions; the AI only answers using the content of your uploaded documents.
</div>
""", unsafe_allow_html=True)

# --- START: Change 4 (Update caption text) ---
st.caption("Upload your knowledge base documents (PDF, TXT, DOCX, etc.) and begin your intelligent data exploration.")
# --- END: Change 4 ---

# -------------------------------
# File Upload Section
# -------------------------------
uploaded_files = st.file_uploader(
    "☁📥 **Upload Your Data Vault**", 
    accept_multiple_files=True, 
    # --- START: Change 1 (Accept multiple file types) ---
    type=["pdf", "txt", "docx", "csv", "sql", "pptx", "xlsx"], 
    # --- END: Change 1 ---
    help="Select one or more files. The AI will build a knowledge base from these documents."
)

if uploaded_files:
    # --- START: Change 2 (Rename variable from pdf_paths to generic file_paths) ---
    file_paths = []
    os.makedirs("data", exist_ok=True) 
    
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        file_paths.append(file_path)

    # --- Initialization Logic ---
    pipeline_needs_reinit = (
        "pipeline" not in st.session_state 
        or st.session_state.pipeline is None
    )

    if pipeline_needs_reinit:
        # --- START: Change 4 (Update spinner text) ---
        with st.spinner("Indexing documents... This may take a moment."):
            try:
                # --- START: Change 3 (Pass generic file_paths) ---
                st.session_state.pipeline = RAGPipeline(st.session_state.active_session, file_paths)
                # --- END: Change 3 ---
                st.session_state.history_manager = HistoryManager(st.session_state.active_session)
                st.session_state.chat_history = st.session_state.history_manager.load_history()
            except Exception as e:
                 st.error(f"Error initializing RAG Pipeline: {e}. ")
                 st.stop()
        # --- END: Change 4 ---
    
    pipeline = st.session_state.pipeline
    history_manager = st.session_state.history_manager

    # -------------------------------
    # Display Chat History Function
    # -------------------------------
    def display_chat_history():
        """Displays messages with user on the left and assistant on the right using columns."""
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                # User message on the LEFT
                col1, col2 = st.columns([7, 3]) # 70% width for message, 30% empty space on the right
                with col1:
                    with st.chat_message("user"):
                        st.markdown(content)
            else:
                # Assistant message on the RIGHT
                col1, col2 = st.columns([3, 7]) # 30% empty space on the left, 70% width for message
                with col2:
                    with st.chat_message("assistant"):
                        st.markdown(content)


    # -------------------------------
    # Display Previous Chat
    # -------------------------------
    st.markdown("---")
    
    if len(st.session_state.chat_history) == 0:
        st.markdown("<p style='text-align:center; color:#D1A980; font-weight:600;'>🎯 Ready to focus! Ask your first question below.</p>", unsafe_allow_html=True)
    else:
        # CALL THE NEW DISPLAY FUNCTION HERE
        display_chat_history()


    # -------------------------------
    # Chat Input & Processing
    # -------------------------------
    user_query = st.chat_input("❓ What question do you have about your uploaded documents?")

    if user_query:
        if user_query != st.session_state.get("last_user_query", None):
            st.session_state.last_user_query = user_query
            
            # The message below will be added to history and displayed via rerun
            
            # Process the AI response
            # --- START: Change 4 (Update spinner text) ---
            with st.spinner("Thinking... Retrieving knowledge from your documents..."):
            # --- END: Change 4 ---
                try:
                    answer = pipeline.ask(user_query) 
                except Exception as e:
                    answer = f"**Error:** Could not get an answer from the your uploaded document. ({e})"
                    st.error(answer)
                
            # 3. Update and Persist History
            history_manager.save_turn("user", user_query)
            history_manager.save_turn("assistant", answer)

            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.session_state.sessions[st.session_state.active_session] = st.session_state.chat_history

            # 4. 🧠 Auto-rename session based on first question
            if "Untitled Chat" in st.session_state.active_session or st.session_state.active_session.startswith("session_"):
                suggested_name_base = user_query.split()[:4]
                suggested_name = " ".join(suggested_name_base).capitalize() + "..."
                
                if len(suggested_name.strip()) > 5:
                    new_name = st.session_state.session_manager.rename_session(
                        st.session_state.active_session, suggested_name
                    )
                    st.session_state.active_session = new_name
                    st.session_state.chat_history = st.session_state.sessions[new_name]
                    st.rerun()
                else:
                    # If no rename, still rerun to display the new messages properly aligned
                    st.rerun()
            else:
                st.rerun()
        else:
            st.stop()
            
else:
    # Initial state message
    st.markdown("---")
    # --- START: Change 4 (Update info message) ---
    st.info("📘 **Awaiting Documents:** Please upload your files (PDFs, DOCX, TXT, etc.) above. Once uploaded, your knowledge base will be indexed and ready for questioning. Your session history is automatically managed on the left.")
    # --- END: Change 4 ---

# -------------------------------
# Custom Footer
# -------------------------------
st.markdown("<p class='footer'> Made With 💚 By Sanchita Bagde. </p>", unsafe_allow_html=True)
