from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class SOP(BaseModel):
    purpose: str
    scope: str
    responsibilities: list[str]
    procedure: list[str]
    escalation: str
    review: str

load_dotenv()

client = OpenAI()

llm = ChatOpenAI(
    model="gpt-4.1-mini"
).with_structured_output(SOP)

print("Welcome to AI Business Operations Assistant!")

user_question = input("Ask your question: ")

instructions = """
You are an AI Business Operations Assistant.

Your job is to help businesses with:
- Creating SOPs
- Summarizing business information
- Answering operational questions
- Improving business processes

When the user asks you to create an SOP, always include:
1. Purpose
2. Scope
3. Responsibilities
4. Procedure
5. Escalation
6. Review

Give clear, practical, and professional answers.
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", instructions),
    ("user", "{user_question}")
])

formatted_messages = prompt.format_messages(
    user_question=user_question
)

chain = prompt | llm

chain_response = chain.invoke({
    "user_question": user_question
})

print()
print("LangChain structured response:")
print(chain_response)

response = client.responses.parse(
    model="gpt-4.1-mini",
    instructions=instructions,
    input=formatted_messages[1].content,
    text_format=SOP
)

sop = response.output_parsed

print()
print("AI Assistant:")
print(sop.scope)




    