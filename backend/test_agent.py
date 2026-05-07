import asyncio

from agents.base.graph import app


async def run_task(task: str):

    initial_state = {
        "task": task,
        "agent_name": "",
        "next_agent": "",
        "messages": [],
        "result": "",
        "status": "running"
    }

    result = await app.ainvoke(initial_state)

    print("\n====================")
    print(f"TASK: {task}")
    print("====================")
    print(result)


async def main():

    tasks = [

        "Research latest AI trends",

        "Send email to client",

        "Update CRM lead status",

        "Generate weekly sales report",

        "Schedule meeting tomorrow"

    ]

    for task in tasks:
        await run_task(task)


asyncio.run(main())