# Import necessary libraries

import os  
# For file and directory operations
import pickle  
# For saving and loading Python objects (used for caching)
from langchain.text_splitter import RecursiveCharacterTextSplitter  
# For splitting text into chunks
from langchain_community.vectorstores import FAISS  
# For creating and managing FAISS vector stores
from langchain_community.embeddings import HuggingFaceEmbeddings  
# For generating embeddings using Hugging Face models
from langchain_community.document_loaders import PyPDFLoader  
# For loading and reading PDF files

class VectorStoreManager:
    """
    A manager class that handles loading, building, and caching FAISS vector stores
    from PDF documents. It automatically detects when PDFs have changed and 
    rebuilds the vector store accordingly.
    """

    def __init__(self, cache_dir="faiss_cache"):
        """
        Initialize the VectorStoreManager with cache directory paths.
        Creates necessary cache directories if they don't exist.

        Args:
            cache_dir (str): Directory to store FAISS and metadata cache files.
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)  # Ensure cache directory exists
        self.cache_file = os.path.join(self.cache_dir, "kb_index.pkl")  # Path to FAISS index cache
        self.metadata_file = os.path.join(self.cache_dir, "pdf_metadata.pkl")  # Path to PDF metadata cache

    def _get_pdf_metadata(self, pdf_files):
        """
        Retrieve metadata (last modified timestamps) for each PDF file.

        Args:
            pdf_files (list): List of PDF file paths.

        Returns:
            dict: A mapping of {pdf_file: last_modified_time}.
        """
        return {pdf: os.path.getmtime(pdf) for pdf in pdf_files}

    def _has_pdf_changed(self, pdf_files):
        """
        Check if any of the provided PDF files have changed since the last cache.

        Args:
            pdf_files (list): List of PDF file paths.

        Returns:
            bool: True if PDFs have changed or no cached metadata exists.
        """
        current_metadata = self._get_pdf_metadata(pdf_files)

        # If no metadata cache exists, treat as changed
        if not os.path.exists(self.metadata_file):
            return True  

        # Load previously saved metadata
        with open(self.metadata_file, "rb") as f:
            cached_metadata = pickle.load(f)

        # Compare current metadata with cached metadata
        return cached_metadata != current_metadata

    def load_or_create_vectorstore(self, pdf_files, rebuild=False):
        """
        Load an existing FAISS vector store from cache or build a new one from PDFs.
        Automatically rebuilds if PDFs have changed or if explicitly requested.

        Args:
            pdf_files (list): List of PDF file paths to process.
            rebuild (bool): Force rebuild even if cache exists.

        Returns:
            FAISS: The loaded or newly built FAISS vector store.
        """
        # Check if rebuild is necessary due to file changes or manual request
        if rebuild or self._has_pdf_changed(pdf_files):
            print("[INFO] Rebuilding vectorstore due to PDF changes or rebuild request...")
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)  # Remove old cached FAISS index

        # If cache exists, load and return it
        if os.path.exists(self.cache_file):
            print("[INFO] Loading cached vectorstore...")
            with open(self.cache_file, "rb") as f:
                vectorstore = pickle.load(f)
            print(f"[INFO] Loaded vectorstore with {len(vectorstore.index_to_docstore_id)} vectors.")
            return vectorstore

        # Otherwise, build a new vector store from scratch
        print("[INFO] Building vectorstore from PDFs...")
        docs = []

        # Load all PDF documents using PyPDFLoader
        for file in pdf_files:
            print(f"[INFO] Loading PDF: {file}")
            loader = PyPDFLoader(file)
            pdf_docs = loader.load()  # Load pages as separate documents
            print(f"[INFO] {len(pdf_docs)} pages loaded from {file}")
            docs.extend(pdf_docs)

        # Handle case when no documents were loaded
        if not docs:
            print("[WARNING] No documents loaded from PDFs!")
            return None

        # Split the documents into smaller text chunks for embedding
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        print(f"[INFO] Created {len(chunks)} text chunks for embeddings")

        # Generate embeddings using a lightweight Hugging Face model
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Build FAISS vector store from document chunks
        vectorstore = FAISS.from_documents(chunks, embeddings)
        print(f"[INFO] Vectorstore created with {len(vectorstore.index_to_docstore_id)} vectors")

        # Cache the newly created FAISS index for faster future loads
        with open(self.cache_file, "wb") as f:
            pickle.dump(vectorstore, f)
            print(f"[INFO] Vectorstore cached at {self.cache_file}")

        # Save current PDF metadata for change detection next time
        with open(self.metadata_file, "wb") as f:
            pickle.dump(self._get_pdf_metadata(pdf_files), f)

        return vectorstore
