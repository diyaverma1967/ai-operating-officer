
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")
    vectordb = Chroma(
        persist_directory="data/leadership_pack/chroma_db",
        embedding_function=embedding_model,
    )
    return vectordb
