# --- Imports and Setup ---

import os
from google.genai.agents import Agent, Session, MemoryBank, Tool 
from kaggle_secrets import UserSecretsClient

try:
    GOOGLE_API_KEY = UserSecretsClient().get_secret("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    print("✅ Gemini API key setup complete.")
except Exception as e:
    print(
        f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
    )


# --- 1. Long-Term Memory Setup ---

def setup_internal_knowledge_base():
    """
    Creates and ingests company documents into the Memory Bank (RAG system).
    This simulates the company's internal, proprietary knowledge.
    """
    print("Setting up Internal Knowledge Base...")

    with open("hr_policy.txt", "w") as f:
        f.write("Annual leave policy is 25 days per year. Expense reports must be submitted by the 5th of each month.")

    with open("onboarding_guide.txt", "w") as f:
        f.write("The onboarding process lasts three days. The default office access code is 12345.")

    # List of files to be indexed
    internal_docs = ["hr_policy.txt", "onboarding_guide.txt"]

    # Initialize the Memory Bank and ingest files
    try:
        # The MemoryBank handles the chunking, embedding, and storage of vectors.
        memory_bank = MemoryBank.create(name="InternalDocsBank") 
        memory_bank.ingest_files(internal_docs) 
        print(f"Memory Bank loaded with {len(internal_docs)} documents.")
        return memory_bank
    except Exception as e:
        print(f"Error setting up Memory Bank: {e}")
        return None

# Initialize the internal knowledge base
INTERNAL_KNOWLEDGE_BANK = setup_internal_knowledge_base()


# --- 2. Agent Definitions  ---

search_tool = google_search_tool.GoogleSearchTool()

EXTERNAL_AGENT = Agent(
    name="External Search Agent",
    description="The fallback agent. Searches external sources using Google Search when internal data is insufficient.",
    tools=[search_tool]
)

INTERNAL_AGENT = Agent(
    name="Internal Search Agent",
    description="The primary agent for internal knowledge queries. Uses the company's Memory Bank.",
    memory_bank=INTERNAL_KNOWLEDGE_BANK
)


# --- 3. Sequential Workflow Orchestration ---

def run_enterprise_workflow(user_query: str):

    print(f"\n--- Processing Query: '{user_query}' ---")
    
    # 1. Attempt internal search first 
    internal_session = Session(agent=INTERNAL_AGENT)
    internal_response = internal_session.send_message(user_query)
    
    if INTERNAL_KNOWLEDGE_BANK and INTERNAL_KNOWLEDGE_BANK.is_grounded(internal_response):
        print("➡️ Internal Agent found a definitive answer.")
        return {
            "source": "Internal Knowledge Bank",
            "response": internal_response.text
        }
    
    # 2. Fallback to external search 
    else:
        print("➡️ Internal Agent failed to find a definitive answer. Falling back to External Search.")
        
        external_session = Session(agent=EXTERNAL_AGENT)
        external_response = external_session.send_message(user_query)
        
        # Add a mandatory warning for external data
        warning = "⚠️ DISCLAIMER: This information comes from external sources and has not been verified by the company."
        
        return {
            "source": "Google Search (External)",
            "response": f"{external_response.text}\n\n{warning}"
        }


# --- Example Execution and Demonstration ---

if __name__ == "__main__":
    # Test Case 1: Internal knowledge query (Should succeed internally)
    query_a = "When are expense reports due?"
    result_a = run_enterprise_workflow(query_a)
    print("\n--- Result A ---")
    print(f"Source: {result_a['source']}")
    print(f"Response: {result_a['response']}")
    
    print("-" * 30)

    # Test Case 2: External/General knowledge query (Should trigger external search)
    query_b = "What were the key stock market trends last week?"
    result_b = run_enterprise_workflow(query_b)
    print("\n--- Result B ---")
    print(f"Source: {result_b['source']}")
    print(f"Response: {result_b['response']}")
