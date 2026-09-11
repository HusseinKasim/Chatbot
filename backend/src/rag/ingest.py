from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src import dependencies
from src import models
import uuid

# Document (PDF) Ingestion
def ingest_doc(uploadedFilePath: Path, db, user, s3_key):
    # Load PDFs
    loader = PyPDFLoader(str(uploadedFilePath))
    documents = loader.load()

    # Extract document title and file type from source
    doc_source_split = Path(documents[0].metadata['source']).name
    doc_title = Path(doc_source_split).stem
    doc_file_type = Path(doc_source_split).suffix.replace('.','')

    # Store documents to db
    new_doc = models.Documents(document_name=doc_title, user_id=int(user['sub']), s3_key=str(s3_key), file_type=doc_file_type)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Split PDFs into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    document_chunks = splitter.split_documents(documents)

    # Get embeddings model
    embeddings = dependencies.get_embeddings_model()

    # Create vectors from embedding model
    vectors = embeddings.embed_documents([chunk.page_content for chunk in document_chunks])

    # Store vectors in pgvector
    for i, chunk in enumerate(document_chunks):
        new_chunk = models.Chunks(document_id=new_doc.id, chunk_id=str(uuid.uuid4()), chunk_text=chunk.page_content, embedding=vectors[i])
        db.add(new_chunk)
        db.commit()
        db.refresh(new_chunk)
    
    return {'document_id': new_doc.id, 'chunks': len(document_chunks)} 