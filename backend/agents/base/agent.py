from abc import ABC, abstractmethod
from typing import List, Callable

from langgraph.graph import StateGraph, END

from agents.base.state import AgentState


class BaseAgent(ABC):

    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: List[Callable] = None
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []

    @abstractmethod
    async def execute(
        self,
        state: AgentState
    ) -> AgentState:
        pass

    async def run(self, task: str):

        workflow = StateGraph(AgentState)

        workflow.add_node(
            self.name,
            self.execute
        )

        workflow.set_entry_point(self.name)

        workflow.add_edge(
            self.name,
            END
        )

        app = workflow.compile()

        initial_state = {
            "task": task,
            "agent_name": self.name,
            "messages": [],
            "result": "",
            "status": "running"
        }

        result = await app.ainvoke(initial_state)

        return result