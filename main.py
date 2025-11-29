import os
import sys
from glob import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# from ingestion import AudioIngestor, DocumentIngestor, PYQIngestor
from ingestion import DocumentIngestor, PYQIngestor 
from embeddings.vector_store import VectorStoreManager
from agent.orchestrator import AgentOrchestrator
from feedback.loop import FeedbackLoop

def main():
    print("=== Multi-Modal RAG Agentic System ===\n")
    
    # 1. Initialize Components
    print("Initializing components...")
    # audio_ingestor = AudioIngestor() # Disabled: Audio ingestion is currently a mock
    doc_ingestor = DocumentIngestor()
    pyq_ingestor = PYQIngestor()
    
    vector_store = VectorStoreManager()
    agent = AgentOrchestrator(vector_store)
    feedback_loop = FeedbackLoop()
    
    # 2. Data Ingestion
    print("\n--- Phase 1: Data Ingestion ---")
    
    # Find PDFs in data directory
    slides_dir = "data/slides"
    pyqs_dir = "data/pyqs"
    
    slide_pdfs = glob(os.path.join(slides_dir, "*.pdf")) if os.path.exists(slides_dir) else []
    pyq_pdfs = glob(os.path.join(pyqs_dir, "*.pdf")) if os.path.exists(pyqs_dir) else []
    
    print(f"Found {len(slide_pdfs)} slide PDF(s) and {len(pyq_pdfs)} PYQ PDF(s)")
    
    if not slide_pdfs and not pyq_pdfs:
        print("\n WARNING: No PDFs found in data/slides or data/pyqs directories!")
        print("Please add PDF files to these directories and run again.")
        return
    
    all_docs = []
    
    for pdf_path in slide_pdfs:
        try:
            chunks = doc_ingestor.ingest(pdf_path)
            all_docs.extend(chunks)
        except Exception as e:
            print(f"  Error ingesting {pdf_path}: {e}")
    
    # Ingest PYQs
    for pdf_path in pyq_pdfs:
        try:
            chunks = pyq_ingestor.ingest(pdf_path)
            all_docs.extend(chunks)
        except Exception as e:
            print(f"  Error ingesting {pdf_path}: {e}")
    
    print(f"\nTotal chunks extracted: {len(all_docs)}")
    
    # 3. Embeddings & Storage
    print("\n--- Phase 2: Embeddings & Storage ---")
    vector_store.add_documents(all_docs)
    
    # 4. Agent Interaction
    print("\n--- Phase 3 & 4: Agent Query Processing ---")
    
    # Example queries
    queries = [
        "Based on the lectures and past exams, predict 3 probable questions for the upcoming exam.",
        "What topics are covered in the course materials?",
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        response = agent.handle_request(query)
        print(f"\nAgent Response:\n{response}\n")
        
        # Optional: Collect feedback
        print("(Feedback collection skipped in demo mode)")
    
    print("\n=== System Run Complete ===")
    print("\nYou can now:")
    print("1. Add more PDFs to data/slides or data/pyqs")
    print("2. Run the system again (it will append to the existing vector store)")
    print("3. Implement interactive query mode for custom questions")

if __name__ == "__main__":
    main()

