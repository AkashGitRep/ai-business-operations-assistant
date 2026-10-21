from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI()


class Complaint(BaseModel):
    customer_name: str
    complaint: str
    priority: str


response = client.responses.parse(
    model="gpt-4.1-mini",
    input="My name is Ravi. My product arrived damaged and this is urgent.",
    text_format=Complaint
)

complaint = response.output_parsed

print("Customer:", complaint.customer_name)
print("Complaint:", complaint.complaint)
print("Priority:", complaint.priority)