from agents.base.agent import BaseAgent
from agents.base.state import AgentState


class SchedulerAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="scheduler_agent",
            system_prompt="""
            You are a scheduling assistant AI.
            Your responsibility is:
            - manage meetings
            - schedule tasks
            - organize calendar events
            - generate reminders
            """
        )

    async def execute(
        self,
        state: AgentState
    ) -> AgentState:

        task = state["task"]

        result = f"""
        Scheduler Agent completed:
        {task}
        """

        state["result"] = result
        state["status"] = "completed"

        return state