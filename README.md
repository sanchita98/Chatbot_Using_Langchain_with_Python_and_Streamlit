#  PDF Chatbot

*A next-gen AI assistant for your PDFs — ask questions, get instant answers, and manage conversations like a pro!*


##  About

The Smart PDF Chatbot is a Generative AI-powered assistant that transforms static PDF documents into an interactive knowledge base.
Ask natural language questions, get context-aware answers, and interact with multiple PDFs without manual searching.

Think of it as **ChatGPT meets your PDF library**.


## 🔍 Why This Project

^ Tired of scrolling PDFs for key information?

^ Want a dynamic Q&A experience with your documents?

^ Need persistent chat sessions to continue your research?

^ This project solves all of that with:

^ RAG (Retrieval-Augmented Generation)

^ FAISS vector storage

^ HuggingFace embeddings

^ Streamlit-based interactive UI


## How It Works 

1. Upload PDFs: Documents loaded and parsed with PyPDFLoader .

2. Text Chunking: Large PDFs split into manageable text chunks. 

3. Vector Embeddings: HuggingFace model generates embeddings. 

4. FAISS Storage: Efficient vector search for retrieving relevant chunks. 

5. LLM Response: GPT, Gemini generates contextual answers. 


## Project Layout 

*app.py -> Streamlit UI & main app

*rag_pipeline.py -> RAGlogic(retrieval + prompt construction)

*vectorstore_manager.py -> FAISS & embeddings 

*chat_OpenAI.py / chat_Gemini.py -> LLM wrappers

*requirements.txt -> Python Dependencies 



###  Create Virtual Environment

python -m venv venv
venv\Scripts\activate    


###  Install Dependencies

pip install -r requirements.txt

###  Add Your API Key

Create a .env file in project root:


OPENAI_API_KEY=your_api_key
# or
GEMINI_API_KEY=your_api_key

###  Run the App

streamlit run app.py

Then open your browser at `http://localhost:8501/


### GitHub  

https://github.com/sanchita98/Chatbot_Using_Langchain_with_Python_and_Streamlit
