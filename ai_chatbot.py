import openai
from typing import List, Dict, Optional
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from chat_history import ChatHistory
from chat_importer import ChatImporter

class AIChatbot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.chat_history = ChatHistory()
        self.chat_importer = ChatImporter(self.chat_history)
        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE
    
    def generate_response(self, user_message: str) -> str:
        """Generate AI response based on user message and chat history"""
        try:
            # Add user message to history
            self.chat_history.add_message('user', user_message)
            
            # Get conversation context
            messages = self.chat_history.get_conversation_context()
            
            # Add system message for context
            system_message = {
                'role': 'system',
                'content': '''You are a helpful AI assistant. Analyze the conversation history to understand context and provide relevant responses. 
                Be conversational, helpful, and maintain context from previous messages.'''
            }
            
            # Prepare messages for API call
            api_messages = [system_message] + messages
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=api_messages,  # type: ignore
                temperature=self.temperature,
                max_tokens=1000
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            if ai_response:
                self.chat_history.add_message('assistant', ai_response)
            
            return ai_response or "No response generated"
            
        except openai.AuthenticationError:
            return "Error: Invalid API key. Please check your OpenAI API key in the configuration."
        except openai.RateLimitError:
            return "Error: Rate limit exceeded. Please wait a moment and try again."
        except openai.APIError as e:
            return f"Error: API error occurred: {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"
    
    def start_new_conversation(self):
        """Start a new conversation"""
        self.chat_history.start_new_conversation()
        return "Started a new conversation. Previous context has been cleared."
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        return self.chat_history.get_conversation_summary()
    
    # Chat import methods
    def import_chat_from_json(self, file_path: str) -> str:
        """Import chat data from JSON file"""
        return self.chat_importer.import_from_json(file_path)
    
    def import_chat_from_csv(self, file_path: str) -> str:
        """Import chat data from CSV file"""
        return self.chat_importer.import_from_csv(file_path)
    
    def import_chat_from_text(self, file_path: str, user_name: str = "User", ai_name: str = "Assistant") -> str:
        """Import chat data from text file"""
        return self.chat_importer.import_from_text(file_path, user_name, ai_name)
    
    def import_manual_conversation(self, conversation_data: List[Dict[str, str]]) -> str:
        """Import conversation data manually provided"""
        return self.chat_importer.import_manual_conversation(conversation_data)
    
    def get_import_formats(self) -> str:
        """Get supported import formats"""
        return self.chat_importer.get_supported_formats() 