from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from src import models
import uuid

load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

# Document (PDF) Ingestion
def ingest_doc(uploadedFilePath: Path, db, user):
    # Load PDFs
    loader = PyPDFLoader(str(uploadedFilePath))
    documents = loader.load()

    # Extract document title and file type from source
    doc_source_split = str(documents[0].metadata['source']).rsplit('\\', 1)[1]
    doc_title = doc_source_split.split('.', 1)[0]

    # Store documents to db
    new_doc = models.Documents(document_name=doc_title, user_id=int(user['sub']))
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Split PDFs into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    document_chunks = splitter.split_documents(documents)

    # Create embedding model
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small',
        api_key=OPENAI_API_KEY
    )

    # Create vectors from embedding model
    vectors = embeddings.embed_documents([chunk.page_content for chunk in document_chunks])

    # Store vectors in pgvector
    for i, chunk in enumerate(document_chunks):
        new_chunk = models.Chunks(document_id=new_doc.id, chunk_id=str(uuid.uuid4()), chunk_text=chunk.page_content, embedding=vectors[i])
        db.add(new_chunk)
        db.commit()
        db.refresh(new_chunk)
    
    return {'document_id': new_doc.id, 'chunks': len(document_chunks)} 