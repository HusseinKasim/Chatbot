from src import models
from langchain_core import documents
from src import dependencies

# Retrieval
async def context_retrieval(prompt, db, user):
    # Get embeddings model
    embeddings = dependencies.get_embeddings_model()
    
    # Search pgvector for similar vectors
    search_result = await similarity_search(query=prompt, k=3, embeddings=embeddings, db=db, user=user)

    # No relevant chunks
    if not search_result:
        return None
    
    # Build context block
    context_block = ''
    for result in search_result:
        context_block+=result.page_content
    
    # Build updated prompt including the chunks
    updated_prompt = f"""
    You are a helpful assistant. Answer the user's question using ONLY the provided document context below. 
    If the user's answer cannot be found in the context, politely state that you do not know.

    [START OF CONTEXT]
    {context_block}
    [END OF CONTEXT]
    
    User question: {prompt}
    Answer:
    """

    # TODO: Add guardrails
    # TODO: add HSNW

    # Return updated prompt
    return updated_prompt


async def similarity_search(query, k, embeddings, db, user):
    # Get query embeddings
    query_embeddings = embeddings.embed_query(query)

    # Cosine distance
    distance = models.Chunks.embedding.cosine_distance(query_embeddings)
    
    # Similarity search in vector db
    chunk_query = (db.query(models.Chunks, distance.label('distance')).join(models.Documents, models.Chunks.document_id == models.Documents.id).filter(models.Documents.user_id == user).order_by(distance).limit(k).all())

    DISTANCE_THRESHOLD = 0.8

    docs = []
    for chunk, chunk_distance in chunk_query:

        # Ignore unrelated chunks
        if chunk_distance > DISTANCE_THRESHOLD:
            continue

        # Return as list of Document objects
        docs.append(documents.Document(
            page_content=chunk.chunk_text,
            metadata={
                'chunk_id': chunk.id,
                'document_id': chunk.document_id
            }
        ))

    return docs
