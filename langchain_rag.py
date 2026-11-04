from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
import chromadb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Initialize the LangChain LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful company support assistant.

Answer the user's question using only the context provided below.

If the answer is not available in the context, say:
"I couldn't find this information in the company documents."

Context:
{context}

Question:
{question}
""")

# Connect to existing Chroma database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Get the existing collection
collection = chroma_client.get_collection(
    name="company_documents"
)

print("Total records:", collection.count())

# LangChain embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Connect LangChain to the existing Chroma collection
vectorstore = Chroma(
    client=chroma_client,
    collection_name="company_documents",
    embedding_function=embeddings
)

print("LangChain connected to existing Chroma database!")

# Create a retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# Format retrieved documents
def format_docs(documents):
    return "\n\n".join(
        document.page_content for document in documents
    )

# Build the RAG chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Test the complete RAG chain
question = "How long does standard shipping take?"

answer = rag_chain.invoke(question)

print("\nFinal Answer:")
print(answer)