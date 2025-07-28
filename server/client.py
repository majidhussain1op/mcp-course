import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from fastmcp.agent import MCPAgent
from fastmcp.client import MCPClient

async def run_memory_chat():
    """Run a memory chat with your FastMCP weather tools."""
    load_dotenv()

    # Path to your FastMCP tool config file
    config_file = "server/weather.json"

    print("Initializing MCP client and Groq LLM...")

    # Load MCP tool definitions from config
    client = MCPClient.from_config_file(config_file)

    # Groq LLM setup (qwen model or mixtral if needed)
    llm = ChatGroq(model="qwen-qwq-32b")

    # MCP Agent with memory support
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)
            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"\nError: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
