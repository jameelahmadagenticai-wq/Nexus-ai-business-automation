from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import pdfplumber
import docx
import pandas as pd

from pydantic import BaseModel

from rag_chain import RAGChain
from text_splitter import DocumentChunker
from vector_store import VectorStore


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# =========================
# CHUNKER
# =========================

chunker = DocumentChunker()

# =========================
# VECTOR STORE
# =========================

vector_store = VectorStore()

# =========================
# RAG CHAIN
# =========================

rag_chain = RAGChain()

# =========================
# QUERY MODEL
# =========================

class QueryRequest(BaseModel):
    query: str

# =========================
# DOCUMENT UPLOAD API
# =========================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    filename = file.filename.lower()

    extracted_text = ""

    # =========================
    # PDF
    # =========================

    if filename.endswith(".pdf"):

        with pdfplumber.open(file.file) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    extracted_text += (
                        text + "\n"
                    )

    # =========================
    # DOCX
    # =========================

    elif filename.endswith(".docx"):

        document = docx.Document(
            file.file
        )

        for paragraph in document.paragraphs:

            extracted_text += (
                paragraph.text + "\n"
            )

    # =========================
    # TXT
    # =========================

    elif filename.endswith(".txt"):

        extracted_text = (
            file.file.read()
            .decode("utf-8")
        )

    # =========================
    # CSV
    # =========================

    elif filename.endswith(".csv"):

        dataframe = pd.read_csv(
            file.file
        )

        extracted_text = (
            dataframe.to_string()
        )

    # =========================
    # UNSUPPORTED FILE
    # =========================

    else:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    # =========================
    # TEXT CHUNKING
    # =========================

    chunks = chunker.split_text(
        extracted_text
    )

    # =========================
    # STORE IN CHROMADB
    # =========================

    vector_store.store_chunks(
        filename=file.filename,
        chunks=chunks
    )

    # =========================
    # RESPONSE
    # =========================

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "message": (
            "Document embedded and "
            "stored successfully"
        )
    }

# =========================
# DOCUMENT QUERY API
# =========================

@router.post("/query")
async def query_documents(
    request: QueryRequest
):

    response = await rag_chain.ask(
        query=request.query
    )

    return response