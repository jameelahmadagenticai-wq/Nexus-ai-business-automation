from agents.base.state import AgentState


class SupervisorAgent:

    async def route_task(
        self,
        state: AgentState
    ) -> AgentState:

        task = state["task"].lower()

        # =========================
        # Routing Logic
        # =========================

        if "email" in task:
            next_agent = "email_agent"

        elif "crm" in task or "lead" in task:
            next_agent = "crm_agent"

        elif "report" in task:
            next_agent = "report_agent"

        elif "schedule" in task or "meeting" in task:
            next_agent = "scheduler_agent"

        else:
            next_agent = "research_agent"

        state["next_agent"] = next_agent

        return state