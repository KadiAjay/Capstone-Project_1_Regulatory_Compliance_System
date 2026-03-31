from src.api.v1.agents.rag_agent import get_rag_agent
import re


def structure_citations(citation_strings: list[str]) -> list[dict]:
    """
    Convert string citations from agent response to structured Citation objects.
    Expected format: "filename - page number"
    Returns: List[{content: str, metadata: {source: str, page: str}}]
    """
    structured = []
    
    # Pattern: "filename - page number" or "filename - page unknown page"
    pattern = r'^(.+?)\s*-\spage\s(.+)$'
    
    for cit_str in citation_strings:
        match = re.match(pattern, cit_str.strip())
        
        if match:
            source = match.group(1).strip()
            page = match.group(2).strip()
        else:
            # Fallback if pattern doesn't match
            source = cit_str.strip()
            page = 'unknown'
        
        structured.append({
            'content': cit_str.strip(),
            'metadata': {
                'source': source,
                'page': page
            }
        })
    
    return structured


def parse_agent_response(response_text):
    """
    Parse the agent's response into structured components.
    Expected format:
    1. Answer: [answer text]
    2. Rule Summary: [summary]
    3. Citations: [citations]
    4. Confidence Score: [score]
    """
    if isinstance(response_text, list):
        response_text = '\n'.join(str(item) for item in response_text)
    elif not isinstance(response_text, str):
        response_text = str(response_text)

    answer = ""
    rule_summary = ""
    citations = []
    confidence_score = 0.5  # default

    # Simple parsing by finding sections
    lines = response_text.split('\n')
    current_section = None
    sections = {'answer': [], 'rule_summary': [], 'citations': [], 'confidence_score': ''}
    
    for line in lines:
        line = line.strip()
        if line.startswith('1. Answer:'):
            current_section = 'answer'
            sections['answer'].append(line.replace('1. Answer:', '').strip())
        elif line.startswith('2. Rule Summary:'):
            current_section = 'rule_summary'
            sections['rule_summary'].append(line.replace('2. Rule Summary:', '').strip())
        elif line.startswith('3. Citations:'):
            current_section = 'citations'
        elif line.startswith('4. Confidence Score:'):
            current_section = 'confidence_score'
            sections['confidence_score'] = line.replace('4. Confidence Score:', '').strip()
        elif current_section and line:
            if current_section == 'citations':
                if line.startswith('- '):
                    sections['citations'].append(line[2:].strip())
            elif current_section in ['answer', 'rule_summary']:
                sections[current_section].append(line)
    
    answer = ' '.join(sections['answer'])
    rule_summary = ' '.join(sections['rule_summary'])
    citations = sections['citations']
    try:
        confidence_score = float(sections['confidence_score'])
    except:
        confidence_score = 0.5

    return {
        'answer': answer,
        'rule_summary': rule_summary,
        'citations': citations,
        'confidence_score': confidence_score
    }


def generate_answer(query: str, regulation_type=None):

    agent = get_rag_agent()

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    final_text = response["messages"][-1].content

    if isinstance(final_text, list):
        final_text = '\n'.join(str(item) for item in final_text)
    elif not isinstance(final_text, str):
        final_text = str(final_text)

    # Parse the structured response
    parsed = parse_agent_response(final_text)
    
    # Fallback if parsing failed
    if not parsed['answer']:
        parsed['answer'] = final_text
        parsed['rule_summary'] = "Key rules extracted from regulatory response."
        parsed['citations'] = []
        parsed['confidence_score'] = 0.9 if "not found" not in final_text.lower() else 0.3

    
    structured_citations = structure_citations(parsed['citations']) if parsed['citations'] else []

    return {
        "query": query,
        "answer": parsed['answer'],
        "citations": structured_citations,
        "rule_summary": parsed['rule_summary'],
        "confidence_score": parsed['confidence_score'],
        "disclaimer": "This response is AI-generated. Please verify with official regulatory documents."
    }