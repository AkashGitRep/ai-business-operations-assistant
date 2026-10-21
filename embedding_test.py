from dotenv import load_dotenv
from openai import OpenAI
import math

load_dotenv()

client = OpenAI()


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


# Load document
with open("knowledge/refund_policy.txt", "r") as file:
    content = file.read()

# Create chunks
chunks = content.split("\n\n")


# Create embeddings for all chunks
chunk_embeddings = []

for chunk in chunks:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )

    embedding = response.data[0].embedding
    chunk_embeddings.append(embedding)


def retrieve_relevant_chunks(question, k=2):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = response.data[0].embedding

    results = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(question_embedding, embedding)

        results.append((score, chunk))

    results.sort(reverse=True)

    return results[:k]


question = "How long do I have to request a refund?"

results = retrieve_relevant_chunks(question, k=2)

for score, chunk in results:
    print(f"Score: {score:.4f}")
    print("Chunk:", chunk)
    print()

# Build context from retrieved chunks
context = "\n\n".join(chunk for score, chunk in results)

prompt = f"""
Answer the user's question using only the information provided below.

Company information:
{context}

User question:
{question}
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

print("Answer:")
print(response.output_text)    