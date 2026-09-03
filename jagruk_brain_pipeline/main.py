from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, START, END

# Import your existing modules
from jagruk_brain_pipeline.input_processor import filter_user_query
from jagruk_brain_pipeline.rag_output_processor import rag_response
from jagruk_brain_pipeline.voice_agent import listen_and_transcribe, speak_response

# 1. Define the Pipeline State
class PipelineState(TypedDict, total=False):
    medium: Literal["1", "2"]  # 1 for Text, 2 for Voice
    raw_query: Optional[str]
    detected_language: Optional[str]  # Added language tracking
    filtered_query: Optional[str]
    final_answer: Optional[str]

# 2. Define the Nodes
def voice_input_node(state: PipelineState):
    print("\n--- Capturing Voice Input ---")
    stt = listen_and_transcribe()
    return {"raw_query": stt}

def filter_query_node(state: PipelineState):
    print("\n--- Filtering Query ---")
    query = state.get("raw_query", "")
    if not query:
        print("Warning: No query provided.")
        return {"filtered_query": "", "detected_language": "English"}
        
    # filter_user_query now returns the 10-field dictionary
    processed_data = filter_user_query(query)
    
    # 1. Get the base English query
    eng_query = processed_data.get("english_query", query)
    
    # 2. Extract the dense search terms and exact product name
    search_terms = processed_data.get("search_terms", [])
    product = processed_data.get("product")
    
    # 3. Combine them to create a hyper-dense vector search string for Qdrant
    dense_query = eng_query
    if product:
        # Clean up the product string (replace underscores with spaces)
        clean_product = product.replace("_", " ")
        dense_query += f" {clean_product}"
        
    if search_terms:
        # Ensure search_terms is treated properly whether it's a list or a string
        if isinstance(search_terms, list):
            dense_query += " " + " ".join(search_terms)
        else:
            dense_query += f" {search_terms}"
            
    lang = processed_data.get("detected_language", "English")
    
    print(f"Detected Language: {lang}")
    print(f"Dense Search Query for Qdrant: {dense_query}")
    
    return {
        "filtered_query": dense_query,
        "detected_language": lang
    }

def rag_response_node(state: PipelineState):
    # Fetch the dense translated query and the original language from state
    filtered = state.get("filtered_query", "")
    target_lang = state.get("detected_language", "English")
    
    # Pass BOTH to the RAG processor
    answer = rag_response(filtered, target_language=target_lang)
    
    return {"final_answer": answer}

def voice_output_node(state: PipelineState):
    print("\n--- Speaking RAG Response ---")
    answer = state.get("final_answer", "")
    if answer:
        # Print to the terminal immediately BEFORE the audio starts playing
        print("\nJAWAAB:")
        print(answer)
        speak_response(answer)
    return {}

# 3. Define the Routing Logic
def route_input(state: PipelineState):
    if state.get("medium") == "2":
        return "voice_input_node"
    else:
        return "filter_query_node"

def route_output(state: PipelineState):
    if state.get("medium") == "2":
        return "voice_output_node"
    else:
        return END

# 4. Build the Graph Architecture
workflow = StateGraph(PipelineState)

workflow.add_node("voice_input_node", voice_input_node)
workflow.add_node("filter_query_node", filter_query_node)
workflow.add_node("rag_response_node", rag_response_node)
workflow.add_node("voice_output_node", voice_output_node)

workflow.add_conditional_edges(
    START, route_input,
    {"voice_input_node": "voice_input_node", "filter_query_node": "filter_query_node"}
)
workflow.add_edge("voice_input_node", "filter_query_node")
workflow.add_edge("filter_query_node", "rag_response_node")
workflow.add_conditional_edges(
    "rag_response_node", route_output,
    {"voice_output_node": "voice_output_node", END: END}
)
workflow.add_edge("voice_output_node", END)

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

        initial_state = {"medium": user_choice}
        
        if user_choice == '1':
            query = input("Enter your query ---> ").strip()
            initial_state["raw_query"] = query

        # Run the pipeline
        final_state = app.invoke(initial_state)

        # Print the final answer here ONLY for the Text route. 
        # (The Voice route already printed it before speaking).
        if user_choice == '1' and final_state.get("final_answer"):
            print("\nJAWAAB:")
            print(final_state["final_answer"])

if __name__ == "__main__":
    main()