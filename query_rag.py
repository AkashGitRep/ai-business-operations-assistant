import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Connect to existing Chroma database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_collection(
    name="company_documents"
)

all_records = collection.get(include=["metadatas"])

print("Total records:", len(all_records["ids"]))
print("Unique IDs:", len(set(all_records["ids"])))

question = "How long does standard shipping take?"

# Create embedding for the question
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

question_embedding = response.data[0].embedding

# Search Chroma
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)

# Provisional relevance threshold for this experiment
MAX_DISTANCE = 1.2

closest_distance = results["distances"][0][0]

if closest_distance > MAX_DISTANCE:
    print("Answer:")
    print("I couldn't find sufficiently relevant information in the available documents.")
    raise SystemExit 

print("Distances:", results["distances"][0])

print("Retrieved chunks:")

for i, document in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}")
   

    metadata = results["metadatas"][0][i] or {}

    if metadata:
        print("Source:", metadata.get("source", "Unknown"))
    else:
        print("Source: Metadata not available")

    print("Distance:", results["distances"][0][i])
    print("Text:", document)


# Build context from retrieved chunks
context = "\n\n".join(results["documents"][0])

# Create prompt for the LLM
prompt = f"""
Answer the user's question using only the information provided below.

Company information:
{context}

User question:
{question}
"""

# Generate answer
answer = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

print("\nAnswer:")
print(answer.output_text)    