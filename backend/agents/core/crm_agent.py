from agents.base.agent import BaseAgent
from agents.base.state import AgentState


class CRMAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="crm_agent",
            system_prompt="""
            You are a CRM management AI.
            Your responsibility is:
            - manage leads
            - track customers
            - update CRM records
            - recommend follow-ups
            """
        )

    async def execute(
        self,
        state: AgentState
    ) -> AgentState:

        task = state["task"]

        result = f"""
        CRM Agent handled:
        {task}
        """

        state["result"] = result
        state["status"] = "completed"

        return state