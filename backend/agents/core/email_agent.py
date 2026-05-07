from agents.base.agent import BaseAgent
from agents.base.state import AgentState

from llm_client import LLMClient


class EmailAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="email_agent",
            system_prompt="""
            You are an AI email assistant.

            Your responsibilities:
            - classify email intent
            - generate professional replies
            - identify support/sales/inquiry emails
            - create concise business responses
            """
        )

    async def execute(
        self,
        state: AgentState
    ) -> AgentState:

        state["agent_name"] = self.name

        task = state["task"]

        # =========================
        # Build Prompt
        # =========================

        prompt = f"""
        You are an enterprise AI email assistant.

        Analyze the following email.

        Determine:
        1. Intent category:
           - support
           - sales
           - inquiry
           - complaint
           - meeting
           - other

        2. Generate a professional reply.

        EMAIL:
        {task}

        Return response in this format:

        Intent: <intent>

        Reply:
        <professional reply>
        """

        # =========================
        # LLM Response
        # =========================

        llm = LLMClient()

        llm_response = await llm.generate(
                prompt=prompt,
                model_type="reasoning"
            )

        # =========================
        # Save Result
        # =========================

        state["result"] = {
        "task": task,
        "ai_response": llm_response
}

        state["status"] = "completed"

        return state