from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class EmailAgentState(TypedDict):
    email_content: str
    extracted_events: List[dict]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def extract_events(email_content: str) -> List[dict]:
    prompt = f"""
    Read this school email and extract important events in JSON format with keys: title, date (YYYY-MM-DD), time (HH:MM if any), notes.

    Email:
    {email_content}
    """
    result = llm.invoke(prompt)
    return [{"raw": line.strip()} for line in result.content.strip().split("\n") if line.strip()]

def run_langgraph_with_email(content: str):
    events = extract_events(content)
    print("📆 Extracted events:")
    for e in events:
        print(" -", e["raw"])
