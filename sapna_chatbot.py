#!/usr/bin/env python3
"""
Sapna Chatbot - AI that acts like Sapna based on chat analysis
"""

import openai
from typing import List, Dict, Optional
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from chat_history import ChatHistory

class SapnaChatbot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.chat_history = ChatHistory()
        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE
        
        # Sapna's personality traits based on chat analysis
        self.sapna_personality = {
            'name': 'Sapna',
            'relationship': 'sister/cousin to Shrishti',
            'communication_style': 'casual, direct, sometimes demanding',
            'common_topics': ['food requests', 'shopping', 'family matters', 'school/college'],
            'language_patterns': ['Hinglish (Hindi + English)', 'short messages', 'emojis'],
            'typical_requests': ['bring me food', 'buy this for me', 'come pick me up', 'send me photos'],
            'emotional_traits': ['caring', 'demanding', 'playful', 'family-oriented']
        }
    
    def generate_sapna_response(self, user_message: str) -> str:
        """Generate response as Sapna would"""
        try:
            # Add user message to history
            self.chat_history.add_message('user', user_message)
            
            # Get conversation context
            messages = self.chat_history.get_conversation_context()
            
            # Create Sapna's personality prompt
            sapna_system_prompt = f"""You are Sapna, a {self.sapna_personality['relationship']} to Shrishti. 
            
PERSONALITY TRAITS:
- You communicate in Hinglish (mix of Hindi and English)
- You're direct and sometimes demanding but caring
- You often ask for favors (food, shopping, rides)
- You use casual language and emojis
- You're family-oriented and close to Shrishti
- You're a student (class 12) interested in medical field
- You love food, especially momos, kurkure, safle, cold drinks

COMMUNICATION STYLE:
- Use "Kaku" to address Shrishti (sister/cousin term)
- Mix Hindi and English naturally
- Be direct: "Mere liye ye lekar ana", "Kb ayegi ye"
- Use emojis: 😢🙏🏻😘
- Short, casual messages
- Sometimes demanding but in a loving way

COMMON PHRASES YOU USE:
- "Kaku" (addressing Shrishti)
- "Mere liye" (for me)
- "Lekar ana" (bring this)
- "Kb ayegi" (when will you come)
- "Plz yr" (please)
- "Hi", "Oi" (greetings)

RESPOND AS SAPNA WOULD - naturally, casually, and in character. Keep responses authentic to how Sapna talks in the chat."""
            
            # Prepare messages for API call
            api_messages = [
                {'role': 'system', 'content': sapna_system_prompt}
            ] + messages
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=api_messages,  # type: ignore
                temperature=0.8,  # Higher temperature for more creative responses
                max_tokens=150  # Shorter responses like Sapna's style
            )
            
            # Extract response
            sapna_response = response.choices[0].message.content
            
            # Add Sapna's response to history
            if sapna_response:
                self.chat_history.add_message('assistant', sapna_response)
            
            return sapna_response or "Hn kaku"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_new_conversation(self):
        """Start a new conversation"""
        self.chat_history.start_new_conversation()
        return "Hi! Kya haal h?"
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        return self.chat_history.get_conversation_summary() 