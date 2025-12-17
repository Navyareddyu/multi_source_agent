# vector_db_indexer.py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings # A free, local embedding model
from langchain_community.vectorstores import Chroma

# 1. Initialize the free embedding model (runs locally)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 

# 2. Load and Split the document
loader = TextLoader("unstructured_data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 3. Create Vector Store
vectorstore = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

vectorstore.persist()
print("Vector database created with RAG documents in ./chroma_db.")