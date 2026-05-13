import pandas as pd
import os
from preprocess import preprocess_text

class ChatbotEngine:
    def __init__(self, dataset_path="symptom_data.csv"):
        self.dataset_path = dataset_path
        self.symptom_db = self._load_data()
        
    def _load_data(self):
        if not os.path.exists(self.dataset_path):
            # Create a fallback dataframe if file doesn't exist yet
            return pd.DataFrame(columns=["symptom", "response", "severity", "emergency"])
        return pd.read_csv(self.dataset_path)
        
    def detect_emergency(self, text):
        emergency_keywords = ["heart attack", "bleeding heavily", "unconscious", "suicide", "stroke", "accident"]
        text_lower = text.lower()
        for kw in emergency_keywords:
            if kw in text_lower:
                return True
        return False
        
    def generate_response(self, user_input):
        # 1. Check for basic greetings
        greetings = ["hi", "hello", "hey", "good morning", "good evening"]
        if user_input.lower().strip() in greetings:
            return "Hello! I am your AI Healthcare Assistant. How can I help you today? Please describe your symptoms."
            
        # 2. Hard emergency check based on keywords
        if self.detect_emergency(user_input):
            return "🚨 EMERGENCY DETECTED: Please call emergency services (e.g., 911 or local emergency number) immediately! Seek urgent medical attention."
            
        # 3. Preprocess input
        tokens = preprocess_text(user_input)
        if not tokens:
            return "Could you please provide more details about how you are feeling?"
            
        # 4. Symptom Matching
        # We will do a simple overlap matching score
        best_match = None
        highest_score = 0
        
        for index, row in self.symptom_db.iterrows():
            db_symptom = row['symptom']
            db_tokens = preprocess_text(db_symptom)
            
            # Count matching tokens
            match_count = sum(1 for token in tokens if token in db_tokens)
            # Also check direct substring match for better accuracy
            if db_symptom.lower() in user_input.lower():
                match_count += 2
                
            if match_count > highest_score:
                highest_score = match_count
                best_match = row
                
        # 5. Return Response
        if best_match is not None and highest_score > 0:
            response_text = best_match['response']
            if best_match['emergency'].lower() == 'yes':
                return f"🚨 EMERGENCY: {response_text}"
            elif best_match['severity'].lower() == 'high':
                return f"⚠️ High Severity: {response_text}"
            else:
                return f"💡 Suggestion: {response_text}"
                
        return "I'm sorry, I couldn't clearly identify the symptom. This chatbot provides general healthcare information only. Please consult a qualified medical professional for an accurate diagnosis."
