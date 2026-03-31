from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.db import get_vector_store

import os
load_dotenv()


def ingest_file(file_path: str, filename: str, regulation_type: str):
    """Ingest PDF/TXT and store in pgvector."""

  
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    docs = loader.load()

    print("pages:", len(docs))

   
    for doc in docs:
        doc.metadata.update({
            "source": filename,
            "document_extension": filename.split(".")[-1],
            "page": doc.metadata.get("page", None),
            "last_updated": os.path.getmtime(file_path),
            "regulation_type": regulation_type  
        })


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(docs)

    print("chunks:", len(chunks))


    vector_store = get_vector_store(collection_name="regulatory-compilance")
    vector_store.add_documents(chunks)

    print("ingestion completed successfully!")


    return {
        "chunks": len(chunks)
    }