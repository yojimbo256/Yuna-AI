from transformers import pipeline

class YunaPersonalityBehavioralStructuring:
    def __init__(self):
        self.style = "neutral"
        self.emotion = "neutral"
        self.tone_adjustment = pipeline("text2text-generation", model="mistral-7b-finetuned")

    def adjust_style(self, user_preference):
        """Adjust Yuna's style based on user preferences"""
        self.style = user_preference.get("style", "neutral")
        self.emotion = user_preference.get("emotion", "neutral")
    
    def generate_response(self, user_input):
        """Generate Yuna's response with adjusted personality"""
        response = self.tone_adjustment(f"Adjust tone for {self.style} and {self.emotion}: {user_input}")
        return response[0]['generated_text']
