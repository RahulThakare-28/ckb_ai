import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

def get_llm_agent(api_key):
    # 1. Initialize Groq Model
    model = ChatGroq(api_key=api_key, model_name="qwen/qwen3-32b")

    # 2. Define Middleware for Clarification (Interrupts)
    # We set it to interrupt when the model wants to call a 'clarify' tool
    # or you can set specific tools that require human approval.
    middleware = [
        HumanInTheLoopMiddleware(
            interrupt_on={
                "clarify_intent": True  # All decisions allowed
            }
        )
    ]

    # 3. Setup Short-term Memory
    memory = InMemorySaver()

    # 4. Create the Agent
    # Note: In a real scenario, you'd define a 'clarify_intent' tool.
    tools = [] # Add your specific tools here
    agent = create_agent(
        model=model,
        tools=tools,
        middleware=middleware,
        checkpointer=memory
    )
    return agent