from dotenv import load_dotenv
import os
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PG_CONNECTION = os.getenv("PG_CONNECTION_STRING")

def get_embeddings():
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

def get_vector_store(collection_name: str = "regulatory-compilance"):
    return PGVector(
        collection_name=collection_name,
        connection=PG_CONNECTION,
        embeddings=get_embeddings(),
        use_jsonb=True
    )

def get_llm():
    return ChatOpenAI(
        model_name=os.getenv("OPENAI_REASONING_MODEL", "gpt-4"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )