import os
import pickle
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredFileLoader



class VectorStoreManager:
    def __init__(self, cache_dir="faiss_cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, "kb_index.pkl")
        # --- START: Change 3 (Rename metadata file) ---
        self.metadata_file = os.path.join(self.cache_dir, "file_metadata.pkl") 

    # --- START: Change 3 (Rename and generalize function) ---
    def _get_file_metadata(self, files):
        """Return a dictionary of {file: last_modified_time} for existing files"""
        # Filter for existing files to prevent errors if a file was deleted
        return {file: os.path.getmtime(file) for file in files if os.path.exists(file)}

    def _has_file_changed(self, files):
        """Check if files have changed since last cache"""
        current_metadata = self._get_file_metadata(files)
        # --- END: Change 3 ---
        if not os.path.exists(self.metadata_file):
            return True  # no previous metadata
        
        try:
            with open(self.metadata_file, "rb") as f:
                cached_metadata = pickle.load(f)
        except Exception:
            # If loading fails (e.g., file corrupted or format change), assume change
            return True
            
        # Compare metadata
        return cached_metadata != current_metadata
    
    # --- START: Change 2 (New helper for dynamic loading) ---
    def _get_loader(self, file_path):
        """Selects the appropriate LangChain DocumentLoader based on file extension."""
        extension = os.path.splitext(file_path)[1].lower()
        
        # Mapping common extensions to specific loaders
        loader_map = {
            ".pdf": PyPDFLoader,
            ".txt": TextLoader,
            ".sql": TextLoader,  # Example: Treating SQL files as text
            ".csv": UnstructuredFileLoader,
            ".docx": UnstructuredFileLoader,
            ".pptx": UnstructuredFileLoader,
        }
        
        # Default to UnstructuredFileLoader for maximum compatibility
        Loader = loader_map.get(extension, UnstructuredFileLoader)
        return Loader(file_path)
    # --- END: Change 2 ---

    # --- START: Change 3 (Rename parameter to generic 'files') ---
    def load_or_create_vectorstore(self, files, rebuild=False):
        """
        Load cached FAISS vectorstore, or create a new one from multiple file types.
        Automatically rebuilds if files have changed.
        """
        # Check if rebuild is needed
        if rebuild or self._has_file_changed(files):
            # --- START: Change 3 (Update print statement) ---
            print("[INFO] Rebuilding vectorstore due to file changes or rebuild request...")
            # --- END: Change 3
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)

        # Load cache if exists
        if os.path.exists(self.cache_file) and not rebuild:
            print("[INFO] Loading cached vectorstore...")
            with open(self.cache_file, "rb") as f:
                vectorstore = pickle.load(f)
            print(f"[INFO] Loaded vectorstore with {len(vectorstore.index_to_docstore_id)} vectors.")
            return vectorstore

        # Build new vectorstore
        # --- START: Change 3 (Update print statement) ---
        print("[INFO] Building vectorstore from files...")
        # --- END: Change 3
        
        docs = []
        # --- START: Change 4 (Update loading loop to handle all files) ---
        for file in files:
            if not os.path.exists(file):
                 print(f"[WARNING] File not found and skipped: {file}")
                 continue
                 
            try:
                # Use the new dynamic loader function
                loader = self._get_loader(file)
                print(f"[INFO] Loading file: {file} using {loader.__class__.__name__}")
                file_docs = loader.load()
                print(f"[INFO] {len(file_docs)} documents loaded from {file}")
                docs.extend(file_docs)
            except Exception as e:
                print(f"[ERROR] Failed to load file {file}. Skipping. Error: {e}")
                continue

        if not docs:
            # --- START: Change 3 (Update print statement) ---
            print("[WARNING] No documents loaded from files!")
            # --- END: Change 3
            return None
        # --- END: Change 4 ---

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        print(f"[INFO] Created {len(chunks)} text chunks for embeddings")

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        print(f"[INFO] Vectorstore created with {len(vectorstore.index_to_docstore_id)} vectors")

        # Cache vectorstore
        with open(self.cache_file, "wb") as f:
            pickle.dump(vectorstore, f)
            print(f"[INFO] Vectorstore cached at {self.cache_file}")

        # Save file metadata
        with open(self.metadata_file, "wb") as f:
            # --- START: Change 3 (Use new generic metadata function) ---
            pickle.dump(self._get_file_metadata(files), f)
            # --- END: Change 3 ---

        return vectorstore





# class VectorStoreManager:
#     def __init__(self, cache_dir="faiss_cache"):
#         self.cache_dir = cache_dir
#         os.makedirs(self.cache_dir, exist_ok=True)
#         self.cache_file = os.path.join(self.cache_dir, "kb_index.pkl")
#         self.metadata_file = os.path.join(self.cache_dir, "pdf_metadata.pkl")

#     def _get_pdf_metadata(self, pdf_files):
#         """Return a dictionary of {pdf_file: last_modified_time}"""
#         return {pdf: os.path.getmtime(pdf) for pdf in pdf_files}

#     def _has_pdf_changed(self, pdf_files):
#         """Check if PDFs have changed since last cache"""
#         current_metadata = self._get_pdf_metadata(pdf_files)
#         if not os.path.exists(self.metadata_file):
#             return True  # no previous metadata
#         with open(self.metadata_file, "rb") as f:
#             cached_metadata = pickle.load(f)
#         # Compare metadata
#         return cached_metadata != current_metadata

#     def load_or_create_vectorstore(self, pdf_files, rebuild=False):
#         """
#         Load cached FAISS vectorstore, or create a new one from PDFs.
#         Automatically rebuilds if PDFs have changed.
#         """
#         # Check if rebuild is needed
#         if rebuild or self._has_pdf_changed(pdf_files):
#             print("[INFO] Rebuilding vectorstore due to PDF changes or rebuild request...")
#             if os.path.exists(self.cache_file):
#                 os.remove(self.cache_file)

#         # Load cache if exists
#         if os.path.exists(self.cache_file):
#             print("[INFO] Loading cached vectorstore...")
#             with open(self.cache_file, "rb") as f:
#                 vectorstore = pickle.load(f)
#             print(f"[INFO] Loaded vectorstore with {len(vectorstore.index_to_docstore_id)} vectors.")
#             return vectorstore

#         # Build new vectorstore
#         print("[INFO] Building vectorstore from PDFs...")
#         docs = []
#         for file in pdf_files:
#             print(f"[INFO] Loading PDF: {file}")
#             loader = PyPDFLoader(file)
#             pdf_docs = loader.load()
#             print(f"[INFO] {len(pdf_docs)} pages loaded from {file}")
#             docs.extend(pdf_docs)

#         if not docs:
#             print("[WARNING] No documents loaded from PDFs!")
#             return None

#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         chunks = splitter.split_documents(docs)
#         print(f"[INFO] Created {len(chunks)} text chunks for embeddings")

#         embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         vectorstore = FAISS.from_documents(chunks, embeddings)
#         print(f"[INFO] Vectorstore created with {len(vectorstore.index_to_docstore_id)} vectors")

#         # Cache vectorstore
#         with open(self.cache_file, "wb") as f:
#             pickle.dump(vectorstore, f)
#             print(f"[INFO] Vectorstore cached at {self.cache_file}")

#         # Save PDF metadata
#         with open(self.metadata_file, "wb") as f:
#             pickle.dump(self._get_pdf_metadata(pdf_files), f)

#         return vectorstore

