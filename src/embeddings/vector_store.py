
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.utils import embedding_functions

class VectorStoreManager:
    def __init__(self, collection_name: str = "kanchan_rag"):
        self.collection_name = collection_name
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Use default embedding function (all-MiniLM-L6-v2)
        # This is a lightweight model that doesn't require OpenAI API
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
        print(f"VectorStoreManager initialized for collection: {collection_name}")
        print(f"  Current document count: {self.collection.count()}")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Adds documents to the vector store.
        documents: List of dicts with 'text' and 'metadata'.
        """
        if not documents:
            print("No documents to add.")
            return
            
        print(f"Adding {len(documents)} documents to vector store...")
        
        # Generate unique IDs based on source and page/index
        ids = []
        texts = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            # Create a unique ID
            source = doc['metadata'].get('source', 'unknown')
            page = doc['metadata'].get('page', i)
            doc_id = f"{os.path.basename(source)}_page_{page}_{i}"
            
            ids.append(doc_id)
            texts.append(doc['text'])
            metadatas.append(doc['metadata'])
        
        # Add to ChromaDB
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"  Successfully added {len(documents)} documents. Total count: {self.collection.count()}")

    def search(self, query: str, top_k: int = 5, weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Performs a weighted search.
        weights: Dict mapping data source type to weight (e.g., {'pyq': 2.0, 'slides': 1.0})
        """
        print(f"Searching for: '{query}' (top_k={top_k})")
        
        # Query ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k * 2, self.collection.count())  # Get more results for reranking
        )
        
        # Convert ChromaDB results to our format
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                doc_text = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                # Convert distance to similarity score (lower distance = higher similarity)
                # ChromaDB uses L2 distance, so we invert it
                similarity = 1 / (1 + distance)
                
                formatted_results.append({
                    "text": doc_text,
                    "metadata": {**metadata, "score": similarity}
                })
        
        # Apply Weighted Fusion Logic
        if weights and formatted_results:
            for res in formatted_results:
                dtype = res['metadata'].get('type')
                weight = weights.get(dtype, 1.0)
                # Adjust score based on document type weight
                res['metadata']['weighted_score'] = res['metadata']['score'] * weight
            
            # Re-sort based on weighted score
            formatted_results.sort(key=lambda x: x['metadata']['weighted_score'], reverse=True)
        else:
            # No weights, just use regular score
            for res in formatted_results:
                res['metadata']['weighted_score'] = res['metadata']['score']
        
        # Return top_k results
        return formatted_results[:top_k]

