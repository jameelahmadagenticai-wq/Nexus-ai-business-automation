import chromadb

from sentence_transformers import (
    SentenceTransformer
)


class VectorStore:

    def __init__(self):

        # =========================
        # CHROMADB CLIENT
        # =========================

        self.client = chromadb.Client()

        # =========================
        # COLLECTION
        # =========================

        self.collection = (
            self.client.get_or_create_collection(
                name="documents"
            )
        )

        # =========================
        # EMBEDDING MODEL
        # =========================

        self.embedding_model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

    # =========================
    # EMBED TEXT
    # =========================

    def create_embedding(
        self,
        text: str
    ):

        embedding = (
            self.embedding_model.encode(
                text
            ).tolist()
        )

        return embedding

    # =========================
    # STORE CHUNKS
    # =========================

    def store_chunks(
        self,
        filename: str,
        chunks: list
    ):

        for index, chunk in enumerate(chunks):

            embedding = self.create_embedding(
                chunk
            )

            self.collection.add(
                ids=[
                    f"{filename}_{index}"
                ],
                documents=[
                    chunk
                ],
                embeddings=[
                    embedding
                ],
                metadatas=[
                    {
                        "filename": filename
                    }
                ]
            )

    # =========================
    # SEARCH DOCUMENTS
    # =========================

    def search_documents(
        self,
        query: str,
        top_k: int = 5
    ):

        # =========================
        # QUERY EMBEDDING
        # =========================

        query_embedding = (
            self.embedding_model.encode(
                query
            ).tolist()
        )

        # =========================
        # CHROMADB SEARCH
        # =========================

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )

        return results