import os
from typing import List, Dict, Any
from pypdf import PdfReader

class DocumentIngestor:
    def __init__(self, use_llama_parse: bool = False):
        self.use_llama_parse = use_llama_parse
        if use_llama_parse:
            # self.parser = LlamaParse(result_type="markdown")
            pass

    def ingest(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Ingests PDF/PPT slides and notes.
        Returns a list of chunks/pages.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Ingesting document {file_path}...")
        
        chunks = []
        
        if self.use_llama_parse:
            # documents = self.parser.load_data(file_path)
            # for doc in documents:
            #     chunks.append({
            #         "text": doc.text,
            #         "metadata": doc.metadata
            #     })
            pass
        else:
            # Use pypdf for extraction
            try:
                reader = PdfReader(file_path)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():  # Only add non-empty pages
                        chunks.append({
                            "text": text,
                            "metadata": {
                                "page": i + 1, 
                                "source": file_path,
                                "type": "slides"
                            }
                        })
                print(f"  Extracted {len(chunks)} pages from {os.path.basename(file_path)}")
            except Exception as e:
                print(f"  Error reading PDF: {e}")
                # Fallback to mock if PDF reading fails
                chunks.append({
                    "text": f"[ERROR] Could not extract content from {os.path.basename(file_path)}",
                    "metadata": {"source": file_path, "type": "slides"}
                })

        return chunks

