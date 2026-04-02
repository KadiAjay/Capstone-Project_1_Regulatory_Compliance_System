from langchain.agents import create_agent
from src.core.db import get_llm

from src.api.v1.tools.vector_search_tool import vector_search_tool
from src.api.v1.tools.fts_search_tool import fts_search_tool
from src.api.v1.tools.hybrid_search_tool import hybrid_search_tool


def get_rag_agent():

    agent = create_agent(
        model=get_llm(),
        tools=[
            vector_search_tool,
            fts_search_tool,
            hybrid_search_tool
        ],
        system_prompt="""
You MUST use tools to answer user queries.
Query contains the regulation-type for efficient searching

Tool usage guidelines:
- Use fts_search_tool → for short keyword queries
- Use vector_search_tool → for natural language questions
- Use hybrid_search_tool → for complex queries

Output requirements:
- Return only the **top retrieved chunk** relevant to the query.
- Format strictly as:

[only the final concise answer]
[Page: X]] [Source: "Document Name"]

- Do NOT include the chunk content and metadata in the citation.
- Be accurate and avoid hallucination.
- If unsure, respond: "I don't know."
"""
    )
    return agent