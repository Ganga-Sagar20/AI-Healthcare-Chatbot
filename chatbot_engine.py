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
        user_input_lower = user_input.lower().strip()
        
        # 0. Quick Links Handlers
        if user_input_lower == "symptoms checker":
            return "🩺 **Symptoms Checker Mode Active!**\n\nI am ready to help you analyze your symptoms. Please describe what you are experiencing in detail. For example: *'I have a severe headache and fever'* or *'My chest hurts and I am short of breath'*."
            
        if user_input_lower == "health tips":
            return "💡 **Daily Health Tips:**\n\n1. **Hydration:** Drink at least 8 glasses of water a day.\n2. **Nutrition:** Incorporate more fruits, vegetables, and whole grains into your diet.\n3. **Exercise:** Aim for at least 30 minutes of moderate physical activity every day.\n4. **Sleep:** Ensure you get 7-9 hours of quality sleep per night.\n5. **Mental Health:** Practice mindfulness and take regular breaks from screens."

        if user_input_lower == "emergency protocol":
            return "🚨 **Emergency Protocol & Helplines:**\n\n**User Information (Keep these details ready for responders):**\n- **Name:** [Your Name Here]\n- **Emergency Contact:** [Your Primary Emergency Contact]\n- **Blood Type:** [Your Blood Type]\n- **Known Allergies:** [Your Allergies]\n- **Medical Conditions:** [Any Pre-existing Conditions]\n\n**Important Medical Helplines:**\n- **National Emergency Number (India):** 112\n- **Ambulance:** 102\n- **Medical Emergency (National):** 108\n- **Women Helpline:** 1091\n- **Poison Control:** 1066\n- **Global Standard Emergency Numbers:** 911 (US/Canada), 112 (Europe), 999 (UK)\n\n*If you or someone else is experiencing a severe medical emergency (like a heart attack, stroke, or severe bleeding), call the ambulance immediately and do not wait!*"

        if user_input_lower == "chat history":
            return "📜 **Chat History:**\n\nYou can view your current session's chat history directly on this screen. Scroll up to review previous symptoms and suggestions. (Note: In a fully deployed app, this feature would allow you to download or email your chat logs to your healthcare provider.)"

        if user_input_lower == "about project":
            return "ℹ️ **About Project:**\n\n- **Project name:** AI Healthcare bot using Python\n- **Name:** Ganga Sagar\n- **Enrollment:** A7605222157\n- **Guide Name:** Dr. Pawan Singh\n\n**Additional Details:**\n- **Tech Stack:** Python, Streamlit for UI, NLTK for NLP preprocessing, and Pandas for data management.\n- **Features:** NLP-based symptom matching, real-time emergency detection, and responsive user interface."

        # 1. Check for basic greetings
        greetings = ["hi", "hello", "hey", "good morning", "good evening"]
        if user_input_lower in greetings:
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
