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
You are a Regulatory Compliance Assistant.

You MUST use tools to answer user queries.

Tool usage guidelines:
- Use fts_search_tool → for short keyword queries
- Use vector_search_tool → for natural language questions
- Use hybrid_search_tool → for complex queries

Output format:
1. Answer: [your answer]
2. Citations:
- source [page]

3. Confidence Score: [0-1 float]

Be accurate and avoid hallucination.
If unsure, say you don't know.
"""
    )

    return agent