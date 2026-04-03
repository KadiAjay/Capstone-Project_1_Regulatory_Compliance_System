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

CRITICAL - OUTPUT FORMAT WITH LINE BREAKS:
You MUST output in this EXACT format - with THREE separate lines separated by newline characters:

Line 1: <answer text here>
Line 2: Page: <page_number>
Line 3: Source: "<source_citation>"

IMPORTANT RULES:
- ALWAYS use actual line breaks between sections
- NEVER put Page and Source on the same line as the answer
- NEVER combine all text into one paragraph
- Each component must be on its own line

EXTRACTION INSTRUCTIONS:
1. Extract the ANSWER: the most relevant concise text from the chunk
2. Extract the PAGE NUMBER: from "page" field in Metadata section
3. Extract the SOURCE CITATION: 
   - Look for regulatory references in the document TEXT (not metadata)
   - Find citations like: "RBI Circular", "RBI Master Direction", "RBI Notification", "SEBI", "Insurance Act", etc.
   - Extract the FULL regulatory citation (e.g., "RBI Circular DBR.No.BP.BC.27/21.04.048/2015-16")
   - DO NOT use filenames like "FAQ.pdf" or "FAQ (1).pdf" as source
   - If cannot find a specific regulatory citation in the content, respond: "It is out of my knowledge."

EXAMPLE (shows line breaks clearly):
Banks must collect KYC documents, a declaration of ownership of gold, loan application, and sanction letter. A passbook or pawn ticket must also be issued to the customer.
Page: 1
Source: "RBI Master Direction on Gold Loans, 2017"

FORMATTING:
- Answer on its own line (can be multiple sentences)
- Page: part on its own line
- Source: part on its own line
- Use \n character to create line breaks if needed
- If page not available, write: Page: N/A
"""
    )
    return agent
