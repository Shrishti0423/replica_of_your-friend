#!/usr/bin/env python3
"""
Generic Chat Replica - Creates AI replicas of anyone based on uploaded chat history
"""

from groq import Groq
from typing import List, Dict, Optional
from config import GROQ_API_KEY, MODEL_NAME
from chat_history import ChatHistory
from chat_importer import ChatImporter
from personality_analyzer import PersonalityAnalyzer

class GenericChatReplica:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.chat_history = ChatHistory()
        self.chat_importer = ChatImporter(self.chat_history)
        self.personality_analyzer = PersonalityAnalyzer()
        self.model_name = MODEL_NAME
        self.temperature = 0.7
        self.person_profile = None
        self.system_prompt = None
        self.person_name = "Person"
    
    def create_replica_from_file(self, file_path: str, file_format: str, person_name: str) -> str:
        """
        Create a chat replica from an uploaded file
        
        Args:
            file_path: Path to the chat file
            file_format: Format type (json, csv, text)
            person_name: Name of the person to replicate
            
        Returns:
            Status message
        """
        try:
            # Import the chat data
            if file_format.lower() == 'json':
                import_msg = self.chat_importer.import_from_json(file_path)
            elif file_format.lower() == 'csv':
                import_msg = self.chat_importer.import_from_csv(file_path)
            elif file_format.lower() == 'text':
                import_msg = self.chat_importer.import_from_text(file_path)
            else:
                return f"Unsupported format: {file_format}"
            
            # Get the imported messages
            messages = self.chat_history.get_conversation_context()
            
            # Analyze the personality
            self.person_profile = self.personality_analyzer.analyze_chat_data(messages, person_name)
            self.person_name = person_name
            
            # Generate system prompt
            self.system_prompt = self.personality_analyzer.generate_system_prompt(self.person_profile, person_name)
            
            profile_summary = self.personality_analyzer.get_profile_summary()
            
            return f"Successfully created {person_name} replica!\n{profile_summary}\n{import_msg}"
            
        except Exception as e:
            return f"Error creating replica: {str(e)}"
    
    def create_replica_from_messages(self, messages: List[Dict[str, str]], person_name: str) -> str:
        """
        Create a chat replica from message list
        
        Args:
            messages: List of message dicts
            person_name: Name of the person
            
        Returns:
            Status message
        """
        try:
            # Import messages
            result = self.chat_importer.import_manual_conversation(messages)
            
            # Get the imported messages
            imported_msgs = self.chat_history.get_conversation_context()
            
            # Analyze personality
            self.person_profile = self.personality_analyzer.analyze_chat_data(imported_msgs, person_name)
            self.person_name = person_name
            
            # Generate system prompt
            self.system_prompt = self.personality_analyzer.generate_system_prompt(self.person_profile, person_name)
            
            profile_summary = self.personality_analyzer.get_profile_summary()
            
            return f"Successfully created {person_name} replica!\n{profile_summary}\n{result}"
            
        except Exception as e:
            return f"Error creating replica: {str(e)}"
    
    def generate_response(self, user_message: str) -> str:
        """
        Generate response as the replicated person
        
        Args:
            user_message: User's input message
            
        Returns:
            Response from the replica
        """
        if not self.system_prompt:
            return "Error: No replica created yet. Please import chat data first."
        
        try:
            # Add user message to history
            self.chat_history.add_message('user', user_message)
            
            # Get conversation context
            messages = self.chat_history.get_conversation_context()
            
            # Prepare messages for API call
            api_messages = [
                {'role': 'system', 'content': self.system_prompt}
            ] + messages
            
            # Call Groq API (same format as OpenAI)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=api_messages,  # type: ignore
                temperature=self.temperature,
                max_tokens=1000
            )
            
            # Extract response
            replica_response = response.choices[0].message.content
            
            # Add to history
            if replica_response:
                self.chat_history.add_message('assistant', replica_response)
            
            return replica_response or "No response generated"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_new_conversation(self):
        """Start a new conversation with the replica"""
        self.chat_history.start_new_conversation()
        return f"Started new conversation with {self.person_name}"
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        return self.chat_history.get_conversation_summary()
    
    def get_profile(self) -> Optional[Dict]:
        """Get the current person's personality profile"""
        return self.person_profile
    
    def get_profile_summary(self) -> str:
        """Get human-readable profile summary"""
        if not self.person_profile:
            return "No profile created yet"
        return self.personality_analyzer.get_profile_summary()
