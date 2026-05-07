from agents.base.agent import BaseAgent
from agents.base.state import AgentState


class ReportAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="report_agent",
            system_prompt="""
            You are a business reporting AI.
            Your responsibility is:
            - create business reports
            - generate analytics summaries
            - prepare executive insights
            - structure formatted reports
            """
        )

    async def execute(
        self,
        state: AgentState
    ) -> AgentState:

        task = state["task"]

        result = f"""
        Report Agent generated report for:
        {task}
        """

        state["result"] = result
        state["status"] = "completed"

        return state