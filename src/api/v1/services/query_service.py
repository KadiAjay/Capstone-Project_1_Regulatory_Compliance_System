
from src.api.v1.agents.rag_agent import get_rag_agent
import re


def generate_answer(query: str, regulation_type= None):
    agent = get_rag_agent()

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}],
        
    })

    # Extract final response text
    final_text = response["messages"][-1].content
    
  

    return {
        "query": query,
        "answer": final_text,
        "raw_output": response
    }


