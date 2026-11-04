
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.messages import ToolMessage

@tool
def get_order_status(order_id: str) -> str:
    """Get the current status of a customer order using its order ID."""

    # Mock order information for learning
    return f"Order {order_id} is currently shipped."


load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

tools = [get_order_status]

llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke(
    "Where is my order ORD101?"
)

print(response.tool_calls)


# Execute the tool and collect its result
tool_messages = []

for tool_call in response.tool_calls:

    tool_result = get_order_status.invoke(tool_call["args"])

    tool_messages.append(
        ToolMessage(
            content=tool_result,
            tool_call_id=tool_call["id"]
        )
    )

# Send the tool result back to the LLM
final_response = llm.invoke(
    [response] + tool_messages
)

print("\nFinal AI Response:")
print(final_response.content)
