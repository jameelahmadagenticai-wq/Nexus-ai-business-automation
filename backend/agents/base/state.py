from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):

    task: str

    agent_name: str

    next_agent: str

    messages: List[Dict[str, Any]]

    result: str

    status: str