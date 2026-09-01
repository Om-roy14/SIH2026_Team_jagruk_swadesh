from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, START, END

# Import your existing modules
from jagruk_brain_pipeline.input_processor import filter_user_query
from jagruk_brain_pipeline.rag_output_processor import rag_response
from jagruk_brain_pipeline.voice_agent import run_voice_agent

# 1. Define the Pipeline State
# Added total=False so partial state updates don't trigger strict typing errors
class PipelineState(TypedDict, total=False):
    medium: Literal["1", "2"]  # 1 for Text, 2 for Voice
    raw_query: Optional[str]
    filtered_query: Optional[str]
    final_answer: Optional[str]

# 2. Define the Nodes
def voice_node(state: PipelineState):
    print("\n--- Starting Voice Assistant ---")
    run_voice_agent()  
    print("\n--- Voice Assistant Finished ---")
    return {}

def filter_query_node(state: PipelineState):
    print("\n--- Filtering Query ---")
    # Safely get the query to prevent KeyErrors
    query = state.get("raw_query", "")
    if not query:
        print("Warning: No query provided.")
        return {"filtered_query": ""}
        
    filtered = filter_user_query(query)
    return {"filtered_query": filtered}

def rag_response_node(state: PipelineState):
    print("--- Fetching RAG Response ---")
    # Safely get the filtered query
    filtered = state.get("filtered_query", "")
    answer = rag_response(filtered)
    return {"final_answer": answer}

# 3. Define the Routing Logic
def route_medium(state: PipelineState):
    # Safely check the medium
    if state.get("medium") == "2":
        return "voice_node"
    else:
        return "filter_query_node"

# 4. Build the Graph Architecture
workflow = StateGraph(PipelineState)

# Add nodes
workflow.add_node("voice_node", voice_node)
workflow.add_node("filter_query_node", filter_query_node)
workflow.add_node("rag_response_node", rag_response_node)

# Add edges and routing
workflow.add_conditional_edges(
    START,
    route_medium,
    {
        "voice_node": "voice_node",
        "filter_query_node": "filter_query_node"
    }
)

# Text path sequence: Filter -> RAG -> END
workflow.add_edge("filter_query_node", "rag_response_node")
workflow.add_edge("rag_response_node", END)

# Voice path sequence: Voice -> END
workflow.add_edge("voice_node", END)

# Compile the application
app = workflow.compile()

# 5. Execution Loop
def main():
    print("Welcome to the Jagruk Brain Pipeline")
    
    while True:
        print("\n" + "="*50)
        user_choice = input("Press '1' for Text, '2' for Voice, or 'q' to Quit: ").strip()
        
        if user_choice.lower() == 'q':
            print("Exiting pipeline...")
            break
            
        if user_choice not in ['1', '2']:
            print("Invalid choice. Please select 1 or 2.")
            continue

        # Prepare the initial state
        initial_state = {"medium": user_choice}
        
        # If text, we need to gather the query before invoking the graph
        if user_choice == '1':
            query = input("Enter your query ---> ").strip()
            initial_state["raw_query"] = query

        # Run the LangGraph application
        final_state = app.invoke(initial_state)

        # Print the final answer if it went through the text route
        if user_choice == '1' and final_state.get("final_answer"):
            print("\nJAWAAB:")
            print(final_state["final_answer"])

if __name__ == "__main__":
    main()