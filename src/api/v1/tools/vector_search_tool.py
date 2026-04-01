from langchain_core.tools import tool
from src.core.db import get_vector_store


@tool
def vector_search_tool(query: str, regulation_type: str = None) -> str:
    """Semantic search using pgvector."""

    vector_store = get_vector_store()

    if regulation_type:
        docs = vector_store.similarity_search(
            query,
            k=5,
            filter={"regulation_type": regulation_type}
        )
    else:
        docs = vector_store.similarity_search(query, k=5)

    if not docs:
        return "No relevant documents found."

    results = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        if page is None:
            page = "unknown"
        content = doc.page_content
        results.append(f"Source: {source} - Page: {page}\nContent: {content}")

    return "\n\n".join(results)