from agents.base.agent import BaseAgent
from agents.base.state import AgentState


class ResearchAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="research_agent",
            system_prompt="""
            You are an AI research specialist.
            Your responsibility is:
            - market research
            - competitor analysis
            - trend analysis
            - summarization
            """
        )

    async def execute(
        self,
        state: AgentState
    ) -> AgentState:

        task = state["task"]

        result = f"""
        Research Agent completed task:
        {task}
        """

        state["result"] = result
        state["status"] = "completed"

        return state