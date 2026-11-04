
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import chromadb

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Connect to existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    client=chroma_client,
    collection_name="company_documents",
    embedding_function=embeddings
)

# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# Test the retriever
test_docs = retriever.invoke(
    "Is shipping free for orders above 1000 rupees?"
)

print("\nRetrieved documents:")

for doc in test_docs:
    print(doc.page_content)

# TOOL 1: Check order status
@tool
def get_order_status(order_id: str) -> str:
    """Get the current status of a customer order."""
    return f"Order {order_id} is currently shipped."


# TOOL 2: Create support ticket
@tool
def create_support_ticket(issue: str) -> str:
    """Create a support ticket for a customer issue."""
    return f"Support ticket created for: {issue}"


# TOOL 3: Check shipping policy
@tool
def check_shipping_policy(question: str) -> str:
    """Search company documents for shipping policy information."""

    documents = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    return context


# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# Register all three tools
tools = [
    get_order_status,
    create_support_ticket,
    check_shipping_policy
]


# Create agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful customer support assistant. Use the available tools when needed to answer customer questions."
)


# Test the agent
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "How long does express shipping take?"}
    ]
})


# Print final response
print(result["messages"][-1].content)
