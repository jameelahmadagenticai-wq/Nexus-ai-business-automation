from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(self):

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=50
            )
        )

    # =========================
    # SPLIT TEXT
    # =========================

    def split_text(
        self,
        text: str
    ):

        chunks = self.text_splitter.split_text(
            text
        )

        return chunks