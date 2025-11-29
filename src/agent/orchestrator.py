import os
from typing import List, Dict, Any
from embeddings.vector_store import VectorStoreManager
import ollama

class AgentOrchestrator:
    def __init__(self, vector_store: VectorStoreManager, model_name: str = None):
        # Allow model selection via environment variable or parameter
        if model_name is None:
            model_name = os.getenv("OLLAMA_MODEL", "llama3.2:1b")  # Default to faster model
        
        self.vector_store = vector_store
        self.model_name = model_name
        
        # Check if Ollama is available
        try:
            ollama.list()
            print(f"✓ Ollama connected. Using model: {model_name}")
        except Exception as e:
            print(f"⚠ WARNING: Ollama not available. Error: {e}")
            print("Please install Ollama and pull a model first.")
            self.model_name = None

    def route_query(self, user_query: str) -> str:
        """
        Decides the intent of the user.
        Returns 'prediction' or 'summary'.
        """
        # Simple keyword based routing for now. 
        # In real app, use an LLM to classify intent.
        if "predict" in user_query.lower() or "question" in user_query.lower() or "exam" in user_query.lower():
            return "prediction"
        return "summary"

    def handle_request(self, user_query: str) -> str:
        intent = self.route_query(user_query)
        print(f"Detected intent: {intent}")
        
        if intent == "prediction":
            return self.generate_prediction(user_query)
        else:
            return self.generate_summary(user_query)

    def generate_prediction(self, query: str) -> str:
        # Phase 2: Weighted Fusion
        # Give higher weight to PYQs for predictions
        weights = {"pyq": 2.0, "slides": 1.0, "audio_transcription": 0.5}
        context = self.vector_store.search(query, top_k=10, weights=weights)
        
        # Phase 3: Context Window Compression
        compressed_context = self.compress_context(context)
        
        # Phase 4: Generate prediction using LLM
        prompt = self.construct_prediction_prompt(query, compressed_context)
        
        if not self.model_name:
            return "[ERROR] Ollama not configured. Please install Ollama and pull a model (e.g., 'ollama pull llama3.2')."
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an educational assistant that helps students prepare for exams by analyzing past questions and course materials."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"[ERROR] Failed to generate prediction: {str(e)}\nMake sure Ollama is running and the model '{self.model_name}' is installed."

    def generate_summary(self, query: str) -> str:
        # Standard RAG weights
        weights = {"slides": 1.5, "audio_transcription": 1.0, "pyq": 0.5}
        context = self.vector_store.search(query, top_k=10, weights=weights)
        
        compressed_context = self.compress_context(context)
        
        if not compressed_context.strip():
            return "[INFO] No relevant content found in the knowledge base for this query."
        
        prompt = f"Based on the following course materials, provide a comprehensive summary for: {query}\n\nCourse Materials:\n{compressed_context}\n\nProvide a clear and concise summary:"
        
        if not self.model_name:
            return "[ERROR] Ollama not configured. Please install Ollama and pull a model (e.g., 'ollama pull llama3.2')."
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant that summarizes course materials for students."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"[ERROR] Failed to generate summary: {str(e)}\nMake sure Ollama is running and the model '{self.model_name}' is installed."

    def compress_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Compresses context to fit token limits.
        """
        if not retrieved_docs:
            return ""
        
        # Simple concatenation for now, but could use summarization or re-ranking.
        context_str = ""
        for doc in retrieved_docs:
            doc_type = doc['metadata'].get('type', 'unknown')
            source = doc['metadata'].get('source', 'unknown')
            page = doc['metadata'].get('page', '?')
            score = doc['metadata'].get('weighted_score', 0)
            
            context_str += f"\n[{doc_type.upper()} - {os.path.basename(source)} p.{page} - relevance: {score:.2f}]\n"
            context_str += f"{doc['text'][:1000]}...\n"  # Truncate long texts
        return context_str

    def construct_prediction_prompt(self, query: str, context: str) -> str:
        return (
            f"Context from past year questions and course materials:\n{context}\n\n"
            f"Student Query: {query}\n\n"
            "Task: You are an expert Computer Architecture professor. Based on the pattern of difficulty, topics, and question types in the past questions (PYQs) and course materials provided above:\n\n"
            "1. Analyze the common themes and difficulty patterns\n"
            "2. Generate 3-5 high-quality probable exam questions that match the pattern\n"
            "3. For each question, provide:\n"
            "   - A clear, well-formatted question\n"
            "   - A comprehensive answer with key concepts\n"
            "   - Any relevant formulas, diagrams descriptions, or examples\n\n"
            "Make the questions challenging but fair, similar to the difficulty level shown in the PYQs."
        )

