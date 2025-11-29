#!/usr/bin/env python3
"""Quick diagnostic script to test Ollama connectivity"""

import ollama

print("Testing Ollama connection...")

try:
    models = ollama.list()
    print(f" Ollama is running")
    print(f" Available models: {[m['name'] for m in models['models']]}")
    
    print("\nTesting llama3.2 response...")
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": "Say 'Hello, I am working!' in one sentence."}
        ]
    )
    print(f" Response: {response['message']['content']}")
    print("\n Ollama is working correctly!")
    
except Exception as e:
    print(f"\n Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure Ollama service is running: ollama serve")
    print("2. Make sure llama3.2 model is installed: ollama pull llama3.2")
