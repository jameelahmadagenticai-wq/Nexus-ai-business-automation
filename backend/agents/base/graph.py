from langgraph.graph import StateGraph, END

from agents.base.state import AgentState

from agents.core.supervisor_agent import SupervisorAgent

from agents.core.research_agent import ResearchAgent
from agents.core.email_agent import EmailAgent
from agents.core.crm_agent import CRMAgent
from agents.core.report_agent import ReportAgent
from agents.core.scheduler_agent import SchedulerAgent


# =========================
# Initialize Agents
# =========================

supervisor = SupervisorAgent()

research_agent = ResearchAgent()
email_agent = EmailAgent()
crm_agent = CRMAgent()
report_agent = ReportAgent()
scheduler_agent = SchedulerAgent()


# =========================
# Create Graph
# =========================

workflow = StateGraph(AgentState)


# =========================
# Add Nodes
# =========================

workflow.add_node(
    "supervisor",
    supervisor.route_task
)

workflow.add_node(
    "research_agent",
    research_agent.execute
)

workflow.add_node(
    "email_agent",
    email_agent.execute
)

workflow.add_node(
    "crm_agent",
    crm_agent.execute
)

workflow.add_node(
    "report_agent",
    report_agent.execute
)

workflow.add_node(
    "scheduler_agent",
    scheduler_agent.execute
)


# =========================
# Entry Point
# =========================

workflow.set_entry_point("supervisor")


# =========================
# Conditional Routing
# =========================

workflow.add_conditional_edges(
    "supervisor",

    lambda state: state["next_agent"],

    {
        "research_agent": "research_agent",
        "email_agent": "email_agent",
        "crm_agent": "crm_agent",
        "report_agent": "report_agent",
        "scheduler_agent": "scheduler_agent",
    }
)


# =========================
# End Edges
# =========================

workflow.add_edge(
    "research_agent",
    END
)

workflow.add_edge(
    "email_agent",
    END
)

workflow.add_edge(
    "crm_agent",
    END
)

workflow.add_edge(
    "report_agent",
    END
)

workflow.add_edge(
    "scheduler_agent",
    END
)


# =========================
# Compile Graph
# =========================

app = workflow.compile()