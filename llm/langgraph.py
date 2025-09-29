from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI

# --- Load environment and initialize LLM ---
load_dotenv()
llm = ChatMistralAI(model_name="mistral-large-latest")

# --- State and Models ---
class ConversationState(TypedDict):
    messages: Annotated[list, add_messages]
    character_response: str
    translation: str
    user_input: str

class CharacterOutput(BaseModel):
    real_reply: str = Field(..., description="Natural human-like response")
    context: str = Field(..., description="Brief context or situation")

class TranslatorOutput(BaseModel):
    translation: str = Field(..., description="Accurate translation")
    confidence: str = Field(..., description="Confidence level: high/medium/low")

# --- Agents ---
def character_agent(state: ConversationState):
    """Simulates natural human conversation with memory."""
    # Get all messages for context (LangGraph automatically accumulates these)
    all_messages = state["messages"]
    
    structured_llm = llm.with_structured_output(CharacterOutput)
    
    # Prepare messages for LLM - include system message + last 10 conversation messages
    messages_for_llm = [
        {"role": "system", "content": """
        You are a friendly, helpful conversation partner who remembers previous interactions.
        Respond naturally and keep the conversation flowing.
        Use the conversation history to maintain context and continuity.
        Reference previous topics when relevant.
        Be engaging and show that you remember what was discussed before.
        """}
    ]
    
    # Add last 10 messages (both user and assistant) for optimal context/token balance
    recent_messages = all_messages[-10:] if len(all_messages) > 10 else all_messages
    messages_for_llm.extend(recent_messages)
    
    response = structured_llm.invoke(messages_for_llm)
    
    # Get the latest user message for state tracking
    user_messages = [msg for msg in all_messages if msg.get("role") == "user"]
    last_user_message = user_messages[-1] if user_messages else {"content": ""}
    
    # Return only the new assistant message - LangGraph will accumulate it
    return {
        "messages": [{"role": "assistant", "content": response.real_reply}],
        "character_response": response.real_reply,
        "user_input": last_user_message.get("content", "")
    }

def translator_agent(state: ConversationState):
    """Translates the character's response."""
    character_response = state.get("character_response", "")
    
    if not character_response:
        return {
            "translation": "No content to translate"
        }
    
    structured_llm = llm.with_structured_output(TranslatorOutput)
    
    response = structured_llm.invoke([
        {"role": "system", "content": f"""
        You are a professional translator.
        Provide an accurate and natural translation into {native_language}.
        Maintain the tone and meaning of the original text.
        Assess your confidence in the translation accuracy.
        """},
        {"role": "user", "content": character_response}
    ])
    
    # Don't add translation to messages - just return the translation data
    return {
        "translation": response.translation
    }

# --- Graph Setup with Persistent Memory ---
def build_graph_with_memory():
    """Build the conversation graph with persistent file-based memory."""
    # Use persistent file-based memory instead of in-memory
    memory = SqliteSaver.from_conn_string("conversation_memory.db")
    
    graph_builder = StateGraph(ConversationState)
    graph_builder.add_node("character", character_agent)
    graph_builder.add_node("translator", translator_agent)
    
    graph_builder.add_edge(START, "character")
    graph_builder.add_edge("character", "translator") 
    graph_builder.add_edge("translator", END)
    
    # Compile with memory checkpointer
    return graph_builder.compile(checkpointer=memory)

# --- Main Execution with Proper State Accumulation ---
if __name__ == "__main__":
    print("🤖 AI Conversation Bot with Memory")
    print("=" * 40)
    
    native_language = input("Enter your native language for translations: ")
    graph = build_graph_with_memory()
    
    # Thread configuration for memory persistence
    thread_config = {"configurable": {"thread_id": "conversation_1"}}
    
    print(f"\nChat started! Translations will be in {native_language}")
    print("Type 'quit' to exit, 'memory' to see conversation history")
    print("-" * 50)
    
    while True:
        user_input = input("\n💬 You: ")
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == 'memory':
            # Show current conversation state
            try:
                current_state = graph.get_state(thread_config)
                messages = current_state.values.get("messages", [])
                print(f"\n📚 Conversation History ({len(messages)} messages):")
                print("-" * 30)
                for i, msg in enumerate(messages[-10:], 1):  # Show last 10 messages
                    role = msg.get("role", "unknown")
                    content = msg.get("content", "")
                    print(f"{i}. {role.title()}: {content}")
                print("-" * 30)
            except Exception as e:
                print(f"❌ Could not retrieve memory: {e}")
            continue
            
        try:
            # Let LangGraph handle state accumulation - just pass the new user message
            result = graph.invoke(
                {"messages": [{"role": "user", "content": user_input}]}, 
                config=thread_config
            )
            
            # Display results
            print(f"🤖 Character: {result['character_response']}")
            if result.get('translation'):
                print(f"🌐 Translation: {result['translation']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

# --- Alternative: In-Memory for Testing ---
def build_graph_with_temp_memory():
    """Use this for testing - memory resets when program ends."""
    memory = SqliteSaver.from_conn_string(":memory:")
    
    graph_builder = StateGraph(ConversationState)
    graph_builder.add_node("character", character_agent)
    graph_builder.add_node("translator", translator_agent)
    
    graph_builder.add_edge(START, "character")
    graph_builder.add_edge("character", "translator")
    graph_builder.add_edge("translator", END)
    
    return graph_builder.compile(checkpointer=memory)
