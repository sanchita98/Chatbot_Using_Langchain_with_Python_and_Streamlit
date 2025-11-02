from vectorstore_manager import VectorStoreManager
from history_manager import HistoryManager
from chat_gemini import ChatGemini


class RAGPipeline:
    def __init__(self, session_id, file_paths):
        """
        Initializes the RAG pipeline components.

        Args:
            session_id (str): The ID of the current chat session.
            file_paths (list): A list of paths to the uploaded document files (PDF, DOCX, TXT, etc.).
        """
        # Load or create the vector store using the generic file paths
        self.vectorstore = VectorStoreManager().load_or_create_vectorstore(file_paths)
        self.history = HistoryManager(session_id)
        self.llm = ChatGemini()



    def ask(self, query):
        """
        Performs Retrieval-Augmented Generation (RAG) to answer a user query.

        Args:
            query (str): The user's question.

        Returns:
            str: The LLM-generated answer based on the retrieved context.
        """
        # 1. Retrieval: Find the top 3 relevant document chunks
        docs = self.vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        
        # 2. History: Format the chat history
        # Note: We load the history *before* the current turn is saved to only provide past context.
        chat_history = "\n".join([f"{h['role']}: {h['content']}" for h in self.history.load_history()])

        # 3. Augmentation & Generation: Construct the prompt
        prompt = f"""
        You are a professional assistant that answers questions based only on the user's uploaded documents.

        Your primary goal:
        - Use the document context below to answer the user's question as accurately as possible.
        - If the answer is NOT found in the provided context, or is only partially related, say clearly:
          "The definition/details are not mentioned directly in the document, but based on related context from the file, here's what can be inferred."

        Rules:
        1. Always prioritize facts and examples found in the context.
        2. Never make up new document content — if it's not there, acknowledge it.
        3. You may provide a short general explanation only AFTER clarifying it's not in the document.
        4. Do NOT mention that you're an AI or language model.

        -----------------------
        📘 Document Context: {context}
        
        Chat history:
        {chat_history}

        Question: {query}
        """

        # 4. Generate the response
        response = self.llm.get_response(prompt)
        
        # NOTE: History saving happens in app.py after the response is received to ensure both the 
        # user query and assistant response are appended together to the session history.
        # Removing the save_turn calls here to prevent duplication, as app.py handles persistence.
        
        return response
