from typing import Dict, Any
import json
import os

class FeedbackLoop:
    def __init__(self, feedback_file: str = "feedback_data.json"):
        self.feedback_file = feedback_file

    def submit_feedback(self, query: str, response: str, rating: int, comments: str = ""):
        feedback_entry = {
            "query": query,
            "response": response,
            "rating": rating,
            "comments": comments
        }
        
        print(f"Saving feedback: {rating} for query '{query}'")
        
        # Append to file
        data = []
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
            except:
                pass
        
        data.append(feedback_entry)
        
        with open(self.feedback_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_high_quality_examples(self):
        if not os.path.exists(self.feedback_file):
            return []
            
        with open(self.feedback_file, 'r') as f:
            data = json.load(f)
            
        return [d for d in data if d['rating'] > 0]
