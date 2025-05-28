import os
import shutil
from pathlib import Path
from collections import defaultdict
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter

CHROMA_DIR = "data/leadership_pack/chroma_db"
RAW_DIR = Path("raw_data")
RAW_DIR.mkdir(exist_ok=True)

splitter = TokenTextSplitter(
    encoding_name="cl100k_base",
    chunk_size=1024,
    chunk_overlap=150
)

def token_count(text):
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")

PERSONAS = {
    "CEO": {
        "pdf": [
            {
                "url": "https://msftstories.thesourcemediaassets.com/2024/05/Satya-Nadella_Transcript_KEY01_Build2024.pdf",
                "local": RAW_DIR / "satya_build2024.pdf"
            }
        ],
        "youtube": [
            {
                "url": "https://www.youtube.com/watch?v=8OviTSFqucI",
                "local": RAW_DIR / "satya_build2024_youtube.txt"
            }
        ],
        "linkedin": [
            {
                "url": "https://www.linkedin.com/in/satyanadella/recent-activity/all/",
                "local": RAW_DIR / "satya_linkedin.txt"
            }
        ]
    },
    "CTO": {
        "pdf": [
            {
                "url": "https://msftstories.thesourcemediaassets.com/2024/05/KevinScott_transcript_KEY01_Build20204.pdf",
                "local": RAW_DIR / "kevin_build2024.pdf"
            }
        ],
        "podcast": [
            {
                "url": "https://www.microsoft.com/en-us/behind-the-tech",
                "local": RAW_DIR / "podcast_kevin.txt"
            }
        ],
        "linkedin": [
            {
                "url": "https://www.linkedin.com/in/kevinscott/recent-activity/all/",
                "local": RAW_DIR / "kevin_linkedin.txt"
            }
        ]
    },
    "EVP_Product": {
        "podcast": [
            {
                "url": "https://blogs.windows.com/windowsexperience/2024/11/19/microsoft-ignite-2024-embracing-the-future-of-windows-at-work",
                "local": RAW_DIR / "pavan_ignite_blog.txt"
            }
        ],
        "youtube": [
            {
                "url": "https://www.youtube.com/watch?v=BSe3qi9Qsxs",
                "local": RAW_DIR / "pavan_ignite_youtube.txt"
            }
        ],
        "linkedin": [
            {
                "url": "https://www.linkedin.com/in/pavandavuluri/recent-activity/all/",
                "local": RAW_DIR / "pavan_linkedin.txt"
            }
        ]
    }
}

def load_and_tag(loader, role, source, url, modality):
    docs = loader.load()
    for doc in docs:
        doc.metadata = {
            "type": modality.upper(),
            "source": os.path.basename(source),
            "url": url,
            "role": role,
            "modality": modality
        }
    return docs

all_documents = []
persona_tokens = defaultdict(lambda: defaultdict(int))
persona_modalities = defaultdict(set)

for role, sources in PERSONAS.items():
    for modality, items in sources.items():
        for entry in items:
            url, local_path = entry["url"], entry["local"]
            try:
                if modality == "pdf" and local_path.exists():
                    docs = load_and_tag(PyPDFLoader(str(local_path)), role, local_path.name, url, modality)
                elif modality in {"youtube", "podcast", "linkedin"} and local_path.exists():
                    docs = load_and_tag(TextLoader(str(local_path), encoding="utf-8"), role, local_path.name, url, modality)
                else:
                    print(f"[WARN] Missing file: {local_path}")
                    continue
                all_documents.extend(docs)
                persona_modalities[role].add(modality)
                print(f"[INFO] Loaded {len(docs)} docs for {role} - {modality}")
                print(f"[DEBUG] Sample metadata: {docs[0].metadata}")
            except Exception as e:
                print(f"[ERROR] Could not ingest {role}-{modality}: {e}")

chunks = splitter.split_documents(all_documents)
for idx, chunk in enumerate(chunks):
    chunk.metadata["chunk_id"] = idx
    chunk.metadata["token_count"] = token_count(chunk.page_content)
    persona = chunk.metadata.get("role")
    modality = chunk.metadata.get("modality")
    persona_tokens[persona][modality] += chunk.metadata["token_count"]

if Path(CHROMA_DIR).exists():
    shutil.rmtree(CHROMA_DIR)

vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding_model, persist_directory=CHROMA_DIR)
vectorstore.persist()

print(f"\n Ingested {len(chunks)} chunks into Chroma DB at: {CHROMA_DIR}")
