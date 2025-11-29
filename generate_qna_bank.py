#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from embeddings.vector_store import VectorStoreManager
from agent.orchestrator import AgentOrchestrator

def extract_topics_from_pdfs():
    slides_dir = "data/slides"
    topics = []
    
    if os.path.exists(slides_dir):
        for filename in os.listdir(slides_dir):
            if filename.endswith('.pdf'):
                # Extract topic from filename (e.g., "M1-a-Intro_motivation.pptx.pdf" -> "Intro motivation")
                topic = filename.replace('.pptx.pdf', '').replace('.pdf', '')
                # Clean up the topic name
                if '-' in topic:
                    parts = topic.split('-')
                    if len(parts) >= 3:
                        topic = ' - '.join(parts[2:])
                topics.append(topic.replace('_', ' '))
    
    if not topics:
        topics = [
            "MIPS Architecture and Instruction Set",
            "Pipeline Processing and Hazards",
            "Branch Prediction",
            "Cache Memory",
            "Memory Hierarchy",
            "Instruction Execution",
            "Control Unit Design"
        ]
    
    return topics

def generate_questions_for_topic(agent, topic, num_questions=10):
    query = f"""Based on the course materials about '{topic}', generate {num_questions} DETAILED SUBJECTIVE exam-style questions.

IMPORTANT REQUIREMENTS:
- DO NOT generate MCQs (multiple choice questions)
- Generate only subjective/descriptive questions that require detailed written answers
- Include a mix of:
  * Conceptual questions (Explain, Describe, Compare)
  * Numerical/calculation problems (with step-by-step solutions)
  * Application-based questions (Apply concepts to scenarios)
  * Analysis questions (Analyze, Evaluate, Why/How questions)

For EACH question, provide:
1. A clear, well-formatted question (worth 5-10 marks)
2. A comprehensive, detailed answer including:
   - Key concepts and definitions
   - Step-by-step explanations
   - Relevant formulas with explanations
   - Diagrams descriptions where applicable
   - Examples to illustrate concepts
   - Common mistakes to avoid

Format each question-answer pair clearly with proper headings."""
    
    print(f"  Generating {num_questions} detailed subjective questions for: {topic}")
    response = agent.handle_request(query)
    return response

def main():
    print("=" * 80)
    print(" Comprehensive Q&A Bank Generator - Exam Preparation Tool")
    print("=" * 80)
    print()
    
    # Configuration
    questions_per_topic = int(input("How many questions per topic? (default: 10): ").strip() or "10")
    output_file = input("Output filename? (default: QnA_Bank.md): ").strip() or "QnA_Bank.md"
    
    print("\n" + "=" * 80)
    print("Initializing RAG system...")
    
    # Initialize components
    vector_store = VectorStoreManager()
    agent = AgentOrchestrator(vector_store)
    
    if not agent.model_name:
        print("\n ERROR: Ollama not available!")
        print("Please start Ollama service: ollama serve")
        return
    
    print(f" Using model: {agent.model_name}")
    print(f" Vector DB has {vector_store.collection.count()} document chunks")
    
    # Extract topics
    print("\n" + "=" * 80)
    print("Extracting topics from course materials...")
    topics = extract_topics_from_pdfs()
    
    print(f"\nFound {len(topics)} topics:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    # Confirm
    print("\n" + "=" * 80)
    confirm = input(f"Generate {questions_per_topic} questions for each topic? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Generate Q&A bank
    print("\n" + "=" * 80)
    print("Generating comprehensive Q&A bank...")
    print("This will take several minutes. Please wait...\n")
    
    # Start markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# Comprehensive Exam Q&A Bank\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Topics:** {len(topics)}\n\n")
        f.write(f"**Questions per Topic:** {questions_per_topic}\n\n")
        f.write("---\n\n")
        
        # Table of Contents
        f.write("##  Table of Contents\n\n")
        for i, topic in enumerate(topics, 1):
            f.write(f"{i}. [{topic}](#{topic.lower().replace(' ', '-').replace('_', '-')})\n")
        f.write("\n---\n\n")
        
        # Generate questions for each topic
        for i, topic in enumerate(topics, 1):
            print(f"[{i}/{len(topics)}] Processing: {topic}")
            
            # Write topic header
            f.write(f"## {i}. {topic}\n\n")
            
            try:
                # Generate questions
                questions_content = generate_questions_for_topic(agent, topic, questions_per_topic)
                f.write(questions_content)
                f.write("\n\n---\n\n")
                
                print(f"  Completed: {topic}\n")
                
            except Exception as e:
                print(f"   Error generating questions for {topic}: {e}\n")
                f.write(f"*Error generating questions for this topic: {e}*\n\n---\n\n")
        
        # Write footer
        f.write("---\n\n")
        f.write("## 🎯 Study Tips\n\n")
        f.write("1. Review questions topic by topic\n")
        f.write("2. Try answering without looking at the answers first\n")
        f.write("3. Focus on understanding concepts, not just memorizing\n")
        f.write("4. Practice numerical problems multiple times\n")
        f.write("5. Review past year questions for question patterns\n\n")
        f.write("**Good luck with your exam! 🚀**\n")
    
    print("\n" + "=" * 80)
    print(f"Q&A Bank generated successfully!")
    print(f"Saved to: {output_file}")
    print(f"Total topics covered: {len(topics)}")
    print(f"Approximate questions: {len(topics) * questions_per_topic}")
    print("\n" + "=" * 80)
    print("\nTip: Open the file in a markdown viewer for better formatting!")
    print(f"   File location: {os.path.abspath(output_file)}\n")

if __name__ == "__main__":
    main()
