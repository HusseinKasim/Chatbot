from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

# Document (PDF) Ingestion
def ingest_doc(uploadedFilePath: Path):
    # Load PDFs
    loader = PyPDFLoader(str(uploadedFilePath))
    document = loader.load()

    # Split PDFs into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    document_chunks = splitter.split_documents(document)

    # Create embeddings
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small',
        api_key=OPENAI_API_KEY
    )

    # Store vectors in pgvector



