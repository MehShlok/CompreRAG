import os
from typing import List, Dict, Any
from pypdf import PdfReader

class PYQIngestor:
    def __init__(self):
        pass

    def ingest(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Ingests Past Year Questions (PYQs).
        These are treated as high-priority data points.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Ingesting PYQ {file_path}...")
        
        # Extract all text from the PDF as PYQs are high priority and context-rich
        questions = []
        
        try:
            reader = PdfReader(file_path)
            # Extract each page as a separate chunk for better granularity
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text.strip():
                    questions.append({
                        "text": text,
                        "metadata": {
                            "source": file_path,
                            "priority": "high",  # Tagged as high priority
                            "page": i + 1,
                            "type": "pyq"
                        }
                    })
            print(f"  Extracted {len(questions)} pages from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  Error reading PYQ PDF: {e}")
            questions.append({
                "text": f"[ERROR] Could not extract content from {os.path.basename(file_path)}",
                "metadata": {"source": file_path, "priority": "high", "type": "pyq"}
            })
        
        return questions

