import os
import asyncio

from agents import Agent, Runner, trace, SQLiteSession, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from openai import AsyncAzureOpenAI
from openai.types.responses import ResponseTextDeltaEvent

from dotenv import load_dotenv
load_dotenv(override=True)

class FIAAgent():
    def __init__(self):
        # Set up the Azure OpenAI client
        self.azure_client = AsyncAzureOpenAI(
                azure_deployment=os.getenv('AZURE_API_MODEL', ''),
                api_key=os.getenv('AZURE_API_KEY', ''),
                api_version=os.getenv('AZURE_API_VERSION', ''),
                azure_endpoint=os.getenv('AZURE_API_BASE', ''),
            )
        
        # Initialize the Azure OpenAI chat completions model
        self.azure_model = OpenAIChatCompletionsModel(
                model=os.getenv('AZURE_API_MODEL', ''),
                openai_client=self.azure_client
            )
        
        # Create a session instance with a session ID
        self.session = SQLiteSession("user_1", "chat_history.db")


    async def chat(self, query: str):
        """Run the chat agent with the given query."""
        params = MCPServerStreamableHttpParams(url="http://localhost:8080/mcp")
        async with MCPServerStreamableHttp(params=params, client_session_timeout_seconds=30) as server:

            agent = Agent(
                name="FIA Agent",
                model=self.azure_model,
                instructions=f"""
                    [Role]
                    You are an FIA (Fire Industry Academy) assistant that helps users find information about students, courses and enrolments in the FIA. FIA specializes exclusively in fire-related training and education.

                    [Responsibilities]
                    You have access to the following tools:
                    - Course Catalog (fire-related courses only)
                    - Student Records
                    - Enrollment Management

                    [Constraints]
                    - Always identify yourself as an FIA assistant.
                    - If you don't know the answer, just say you don't know. Don't try to make up an answer.
                    - If the user asks for personal information, ensure you comply with data privacy regulations.
                    - Provide accurate and concise information.
                    - You must ONLY discuss topics related to FIA fire safety training, firefighting courses, emergency response training, or fire-related enrollments.
                    - FIA does NOT offer programming, science, technology, or any non-fire-related courses. Only fire safety, firefighting, fire prevention, emergency response, and related fire industry training.
                    - If asked about anything unrelated to fire industry training and education, politely redirect the conversation back to fire-related academic matters.
                    """,
                mcp_servers=[server]
            )

            with trace("FIA Agent"):
                result = Runner.run_streamed(agent, query, session=self.session)

                # Stream the response back to the client
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        delta = event.data.delta
                        if delta:
                            yield delta


async def chatbot():
    """Function to run the chat agent."""
    fia = FIAAgent()

    while True:
        # Get user input
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            break
        
        # Generate and print the response
        try:
            print("Assistant: ", end="", flush=True)
            full_response = ""
            async for chunk in fia.chat(user_input):
                print(chunk, end="", flush=True)
                full_response += chunk
            print()
        except Exception as e:
            print("Error:", e)


def main():
    """Main entry point for the chat agent."""
    asyncio.run(chatbot())


if __name__ == "__main__":
    main()