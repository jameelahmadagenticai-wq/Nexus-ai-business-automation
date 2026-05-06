import ollama

from memory_client import (
    retrieve_memories
)

from prompt_template import PromptTemplate

from cache import (
    build_cache_key,
    get_cached_response,
    cache_response
)


class LLMClient:

    def __init__(self):

        # =========================
        # MODEL REGISTRY
        # =========================

        self.models = {
            "reasoning": "llama3",
            "fast": "phi3",
            "code": "mistral"
        }

    # =========================
    # MEMORY HELPERS
    # =========================

    def _retrieve_memory_context(
        self,
        prompt: str
    ):

        try:

            memories = retrieve_memories(
                user_id="1",
                query=prompt
            )

        except Exception:

            memories = []

        memory_context = ""

        for memory in memories:

            memory_text = memory.get(
                "memory",
                ""
            )

            if memory_text:

                memory_context += (
                    f"- {memory_text}\n"
                )

        return memory_context

    # =========================
    # NORMAL GENERATION
    # =========================

    async def generate(
        self,
        prompt: str,
        model_type: str = "fast",
        history: list = None
    ):

        # =========================
        # MODEL SELECTION
        # =========================

        model_name = self.models.get(
            model_type,
            "phi3"
        )

        # =========================
        # RETRIEVE MEMORIES
        # =========================

        memory_context = self._retrieve_memory_context(
            prompt
        )

        # =========================
        # BUILD FINAL PROMPT
        # =========================

        formatted_prompt = (
            PromptTemplate.build_chat_prompt(
                user_message=prompt,
                history=history,
                memory_context=memory_context
            )
        )

        # =========================
        # CACHE CHECK
        # =========================

        cache_key = build_cache_key(
            "llm",
            model_name,
            prompt
        )

        cached_response = get_cached_response(
            cache_key
        )

        if cached_response:

            return cached_response

        # =========================
        # OLLAMA REQUEST
        # =========================

        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": formatted_prompt
                }
            ]
        )

        # =========================
        # AI RESPONSE
        # =========================

        ai_response = (
            response["message"]["content"]
        )

        # =========================
        # SAVE CACHE
        # =========================

        cache_response(
            cache_key,
            ai_response
        )

        return ai_response

    # =========================
    # STREAMING GENERATION
    # =========================

    async def stream_generate(
        self,
        prompt: str,
        model_type: str = "fast",
        history: list = None
    ):

        # =========================
        # MODEL SELECTION
        # =========================

        model_name = self.models.get(
            model_type,
            "phi3"
        )

        # =========================
        # RETRIEVE MEMORIES
        # =========================

        memory_context = self._retrieve_memory_context(
            prompt
        )

        # =========================
        # BUILD FINAL PROMPT
        # =========================

        formatted_prompt = (
            PromptTemplate.build_chat_prompt(
                user_message=prompt,
                history=history,
                memory_context=memory_context
            )
        )

        # =========================
        # CACHE CHECK
        # =========================

        cache_key = build_cache_key(
            "llm",
            model_name,
            prompt
        )

        cached_response = get_cached_response(
            cache_key
        )

        if cached_response:

            yield cached_response
            return

        # =========================
        # STREAM REQUEST
        # =========================

        stream = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": formatted_prompt
                }
            ],
            stream=True
        )

        # =========================
        # FULL RESPONSE HOLDER
        # =========================

        full_response = ""

        # =========================
        # STREAM CHUNKS
        # =========================

        for chunk in stream:

            content = (
                chunk.get("message", {})
                .get("content", "")
            )

            if content:

                full_response += content

                yield content

        # =========================
        # SAVE CACHE
        # =========================

        cache_response(
            cache_key,
            full_response
        )
