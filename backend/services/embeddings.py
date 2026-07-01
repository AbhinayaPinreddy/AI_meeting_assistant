from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="meetings"
)


def store_transcript(meeting_id, transcript):

    embedding = model.encode(transcript).tolist()

    collection.add(
        ids=[str(meeting_id)],
        embeddings=[embedding],
        documents=[transcript]
    )

    print("Embedding Stored Successfully")