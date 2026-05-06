class PromptTemplate:

    # =========================
    # CHAT PROMPT
    # =========================

    @staticmethod
    def build_chat_prompt(
        user_message: str,
        history: list = None,
        memory_context: str = ""
    ):

        # =========================
        # SYSTEM PROMPT
        # =========================

        system_prompt = """
You are NexusOS AI.

You are an autonomous AI assistant specialized in:
- business intelligence
- CRM
- automation
- analytics
- AI workflows
- productivity

Provide:
- clear answers
- concise explanations
- professional responses

Use relevant user memories whenever helpful.
"""

        # =========================
        # HISTORY
        # =========================

        history_text = ""

        if history:

            for message in history:

                role = message.get(
                    "role",
                    "user"
                )

                content = message.get(
                    "content",
                    ""
                )

                history_text += (
                    f"{role}: {content}\n"
                )

        # =========================
        # FINAL PROMPT
        # =========================

        final_prompt = f"""
{system_prompt}

Relevant User Memories:
{memory_context}

Conversation History:
{history_text}

User:
{user_message}

Assistant:
"""

        return final_prompt
