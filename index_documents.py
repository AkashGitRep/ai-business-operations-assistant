
import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    chroma_client.delete_collection(name="company_documents")
except Exception:
    pass

collection = chroma_client.create_collection(
    name="company_documents"
)

knowledge_folder = "knowledge"

for filename in os.listdir(knowledge_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(knowledge_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        chunks = [
            chunk.strip()
            for chunk in content.split("\n\n")
            if chunk.strip()
        ]

        for i, chunk in enumerate(chunks):
            embedding_response = client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            )

            embedding = embedding_response.data[0].embedding

            collection.upsert(
                ids=[f"{filename}_{i}"],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": filename}]
            )

        print(f"Indexed {filename}: {len(chunks)} chunks")

print("All documents indexed successfully!")
print("Total chunks in collection:", collection.count())
