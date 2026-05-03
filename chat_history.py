import json
import os
from datetime import datetime
from typing import List, Dict, Any
from config import CHAT_HISTORY_FILE, MAX_HISTORY

class ChatHistory:
    def __init__(self):
        self.history_file = CHAT_HISTORY_FILE
        self.conversations = self.load_history()
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load chat history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_history(self):
        """Save chat history to file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
    
    def add_message(self, role: str, content: str):
        """Add a new message to the conversation"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to current conversation
        if not self.conversations:
            self.conversations.append([])
        
        self.conversations[-1].append(message)
        
        # Limit history length
        if len(self.conversations[-1]) > MAX_HISTORY * 2:  # *2 because each exchange has 2 messages
            self.conversations[-1] = self.conversations[-1][-MAX_HISTORY * 2:]
        
        self.save_history()
    
    def get_conversation_context(self) -> List[Dict[str, str]]:
        """Get the current conversation as context for AI"""
        if not self.conversations:
            return []
        
        # Convert to OpenAI format (role, content)
        context = []
        for message in self.conversations[-1]:
            context.append({
                'role': message['role'],
                'content': message['content']
            })
        return context
    
    def start_new_conversation(self):
        """Start a new conversation"""
        self.conversations.append([])
        self.save_history()
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversations or not self.conversations[-1]:
            return "No conversation history."
        
        messages = self.conversations[-1]
        summary = f"Conversation has {len(messages)} messages:\n"
        
        for i, msg in enumerate(messages[-6:], 1):  # Show last 6 messages
            role = "User" if msg['role'] == 'user' else "Assistant"
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            summary += f"{i}. {role}: {content}\n"
        
        return summary 