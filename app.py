from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import json
import chromadb

load_dotenv()

app = FastAPI()
client = OpenAI()

def retrieve_relevant_chunks(question, k=2):
    # Create an embedding for the user's question
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = response.data[0].embedding

    # Search Chroma for relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )

    # Check whether any retrieved result is sufficiently relevant
    max_distance = 1.2
    closest_distance = results["distances"][0][0]

    if closest_distance > max_distance:
        return []

    return results["documents"][0]

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_collection(
    name="company_documents"
)

class BusinessRequest(BaseModel):
    name: str
    industry: str

class AskRequest(BaseModel):
    question: str

@app.get("/hello")
def hello():
    return {"message": "Hello from AI Business Operations Assistant"}

@app.post("/business")
def create_business(business: BusinessRequest):
    return {
        "name": business.name,
        "industry": business.industry
    }    

def get_order_status(order_id):
    return "Shipped" 

def create_support_ticket(issue):
    return "Support ticket created"

tools = [
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Get the current status of an order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string"
                }
            },
            "required": ["order_id"],
            "additionalProperties": False
        }
    },
    
    {
    "type": "function",
    "name": "create_support_ticket",
    "description": "Create a support ticket for a customer issue.",
    "parameters": {
        "type": "object",
        "properties": {
            "issue": {
                "type": "string",
                "description": "The customer's problem or complaint."
            }
        },
        "required": ["issue"],
        "additionalProperties": False
    }
}

]




@app.post("/ask")
def ask(request: AskRequest):
    question = request.question.lower()

    # Step 1: Route order and support requests to tools
    action_phrases = [
        "order status",
        "status of order",
        "track order",
        "where is my order",
        "support ticket",
        "create a ticket",
        "report a problem"
    ]

    if any(phrase in question for phrase in action_phrases):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=request.question,
            tools=tools
        )

        for item in response.output:
            if item.type == "function_call":
                arguments = json.loads(item.arguments)

                if item.name == "get_order_status":
                    result = get_order_status(arguments["order_id"])
                elif item.name == "create_support_ticket":
                    result = create_support_ticket(arguments["issue"])
                else:
                    result = "Unknown tool"

                final_response = client.responses.create(
                    model="gpt-4.1-mini",
                    previous_response_id=response.id,
                    input=[{
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result
                    }]
                )

                return {"answer": final_response.output_text}

        return {"answer": response.output_text}

    # Step 2: Retrieve relevant company information
    chunks = retrieve_relevant_chunks(request.question)

    if not chunks:
        return {
            "answer": "I couldn't find this information in the available company documents."
        }

    context = "\n\n".join(chunks)

    prompt = f"""
Answer the user's question using only the company information below.
If the information does not answer the question, say so.
Do not invent company policies.

Company information:
{context}

User question:
{request.question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {"answer": response.output_text}
