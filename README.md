# AI Business Operations Assistant

An AI-powered business operations assistant built with Python, OpenAI, LangChain, and FastAPI concepts. The project explores how Large Language Models can help businesses generate Standard Operating Procedures (SOPs), retrieve relevant knowledge, and automate operational tasks.

## Features

- **AI-Powered SOP Generation:** Generate structured Standard Operating Procedures using Pydantic models and LLMs.
- **Structured Outputs:** Convert natural-language requests into validated, structured responses.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant information from business documents to support context-aware answers.
- **Embeddings and Vector Search:** Generate document embeddings and retrieve semantically relevant content using ChromaDB.
- **LangChain Integration:** Use prompt templates and model chains to structure LLM workflows.
- **AI Agent and Tools:** Explore tool-based execution and agent workflows for business operations.
- **Business Knowledge Base:** Use sample policy documents, including shipping and refund policies.

## Technology Stack

- Python
- OpenAI API
- LangChain
- LangChain Core
- LangChain OpenAI
- FastAPI
- Pydantic
- ChromaDB
- Vector Embeddings

## Project Structure

```text
ai-business-operations-assistant/
│
├── knowledge/
│   ├── refund_policy.txt
│   └── shipping_policy.txt
│
├── app.py
├── main.py
├── embedding_test.py
├── index_documents.py
├── query_rag.py
├── read_document.py
├── structured_test.py
├── langchain_rag.py
├── langchain_tools.py
├── langchain_agent.py
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AkashGitRep/ai-business-operations-assistant.git
cd ai-business-operations-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

Install the packages required by the project:

```bash
pip install openai python-dotenv pydantic fastapi uvicorn chromadb langchain langchain-openai langchain-core
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Never commit your actual API key or `.env` file to GitHub.

## Running the Project

Run the relevant Python module depending on the functionality you want to explore:

```bash
python main.py
```

```bash
python langchain_rag.py
```

```bash
python langchain_tools.py
```

```bash
python langchain_agent.py
```

For the FastAPI application, if `app.py` exposes the FastAPI instance as `app`, run:

```bash
uvicorn app:app --reload
```

## Learning Outcomes

This project demonstrates practical implementation and experimentation with:

- LLM integration using the OpenAI API
- Prompt engineering and prompt templates
- Pydantic-based structured outputs
- Text embeddings and semantic search
- Document indexing and retrieval
- Retrieval-Augmented Generation (RAG)
- LangChain chains, tools, and agent workflows

## Future Enhancements

- Conversation memory
- LangGraph-based agent workflows
- Multi-agent collaboration
- Authentication and role-based access
- Docker-based deployment
- Monitoring and evaluation

## Author

**Akash N**

AI Engineer | Generative AI | LLM Applications | RAG | AI Agents | Python

[GitHub](https://github.com/AkashGitRep) · [LinkedIn](https://www.linkedin.com/)

---

*This is a hands-on learning and implementation project focused on applying Generative AI to real-world business operations.*
