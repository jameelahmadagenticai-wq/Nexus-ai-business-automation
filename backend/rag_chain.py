from llm_client import LLMClient

from vector_store import VectorStore


class RAGChain:

    def __init__(self):

        self.vector_store = (
            VectorStore()
        )

        self.llm = LLMClient()

    # =========================
    # ASK QUESTION
    # =========================

    async def ask(
        self,
        query: str
    ):

        # =========================
        # RETRIEVE CHUNKS
        # =========================

        results = (
            self.vector_store.search_documents(
                query=query,
                top_k=5
            )
        )

        documents = results["documents"][0]

        # =========================
        # BUILD CONTEXT
        # =========================

        context = "\n\n".join(
            documents
        )

        # =========================
        # FINAL PROMPT
        # =========================

        rag_prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{query}

Provide:
- concise answer
- accurate response
- cite relevant context
"""

        # =========================
        # GENERATE ANSWER
        # =========================

        answer = await self.llm.generate(
            prompt=rag_prompt,
            model_type="reasoning"
        )

        # =========================
        # RESPONSE
        # =========================

        return {
            "answer": answer,
            "sources": documents
        }