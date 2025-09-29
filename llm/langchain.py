import getpass
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from tools import search_tool, wiki_tool, save_tool
import os

# Load environment variables
load_dotenv()

# Set up API key
if not os.environ.get("MISTRAL_API_KEY"):
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

from langchain_mistralai import ChatMistralAI

# Initialize LLM
llm = ChatMistralAI(model_name="mistral-large-latest")

# Define response structure
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Create memory buffer
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="query",
    output_key="output"
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a research assistant that will help generate a research paper.
    You have access to previous conversation history to maintain context.
    Answer the user query and use necessary tools.
    Wrap the output in this format and provide no other text\n{format_instructions}
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

# Define tools
tools = [search_tool, wiki_tool, save_tool]

# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Create agent executor with memory
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
    return_intermediate_steps=True
)

query=input("ask somthings")

# Get response from agent
raw_response = agent_executor.invoke({"query": query})
            
if isinstance(raw_response.get("output"), str):
    structured_response = parser.parse(raw_response["output"])
else:
    # Handle case where output might be in a different format
    output_text = str(raw_response.get("output", ""))
    structured_response = parser.parse(output_text)

