#!/usr/bin/env python3
"""
Interactive Query Interface for RAG Agent
Ask questions directly to your course materials!
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from embeddings.vector_store import VectorStoreManager
from agent.orchestrator import AgentOrchestrator

def print_banner():
    print("=" * 70)
    print(" Interactive RAG Agent - Ask Me Anything! ")
    print("=" * 70)
    print("Your course materials are loaded and ready!")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.\n")

def main():
    print_banner()
    
    print("Loading vector database...")
    vector_store = VectorStoreManager()
    
    print("Connecting to Ollama...")
    agent = AgentOrchestrator(vector_store)
    
    if not agent.model_name:
        print("\n ERROR: Ollama not available!")
        print("Please start Ollama service: ollama serve")
        return
    
    print(f"\n Ready! Using model: {agent.model_name}")
    print(f" Vector DB has {vector_store.collection.count()} document chunks\n")
    print("-" * 70)
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n Your Question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n Goodbye! Happy studying!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process query
            print("\n Thinking...")
            response = agent.handle_request(user_input)
            
            # Display response
            print("\n" + "=" * 70)
            print(" Answer:")
            print("=" * 70)
            print(response)
            print("=" * 70)
            
        except KeyboardInterrupt:
            print("\n\n Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n Error: {e}")
            print("Please try again with a different question.\n")

if __name__ == "__main__":
    main()
