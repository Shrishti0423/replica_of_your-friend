import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime
from chat_history import ChatHistory

class ChatImporter:
    def __init__(self, chat_history: ChatHistory):
        self.chat_history = chat_history
    
    def import_from_json(self, file_path: str) -> str:
        """Import chat data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON formats
            if isinstance(data, list):
                # Format: [{"role": "user", "content": "...", "timestamp": "..."}, ...]
                self._process_messages(data)
            elif isinstance(data, dict):
                # Format: {"conversations": [[messages], [messages]]}
                if 'conversations' in data:
                    for conv in data['conversations']:
                        self._process_messages(conv)
                elif 'messages' in data:
                    self._process_messages(data['messages'])
            
            return f"✅ Successfully imported {len(data) if isinstance(data, list) else 'multiple'} messages from {file_path}"
            
        except Exception as e:
            return f"❌ Error importing from {file_path}: {str(e)}"
    
    def import_from_csv(self, file_path: str) -> str:
        """Import chat data from CSV file"""
        try:
            messages = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Expected columns: role, content, timestamp (optional)
                    if 'role' in row and 'content' in row:
                        message = {
                            'role': row['role'],
                            'content': row['content'],
                            'timestamp': row.get('timestamp', datetime.now().isoformat())
                        }
                        messages.append(message)
            
            self._process_messages(messages)
            return f"✅ Successfully imported {len(messages)} messages from {file_path}"
            
        except Exception as e:
            return f"❌ Error importing from {file_path}: {str(e)}"
    
    def import_from_text(self, file_path: str, user_name: str = "User", ai_name: str = "Assistant") -> str:
        """Import chat data from plain text file"""
        try:
            messages = []
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Try to parse different formats
                if line.startswith(f"{user_name}:"):
                    content = line[len(f"{user_name}:"):].strip()
                    messages.append({
                        'role': 'user',
                        'content': content,
                        'timestamp': datetime.now().isoformat()
                    })
                elif line.startswith(f"{ai_name}:"):
                    content = line[len(f"{ai_name}:"):].strip()
                    messages.append({
                        'role': 'assistant',
                        'content': content,
                        'timestamp': datetime.now().isoformat()
                    })
                elif ":" in line:
                    # Generic format: "Speaker: message"
                    speaker, content = line.split(":", 1)
                    role = 'user' if speaker.strip().lower() == user_name.lower() else 'assistant'
                    messages.append({
                        'role': role,
                        'content': content.strip(),
                        'timestamp': datetime.now().isoformat()
                    })
            
            self._process_messages(messages)
            return f"✅ Successfully imported {len(messages)} messages from {file_path}"
            
        except Exception as e:
            return f"❌ Error importing from {file_path}: {str(e)}"
    
    def import_manual_conversation(self, conversation_data: List[Dict[str, str]]) -> str:
        """Import conversation data manually provided"""
        try:
            self._process_messages(conversation_data)
            return f"✅ Successfully imported {len(conversation_data)} messages"
        except Exception as e:
            return f"❌ Error importing conversation: {str(e)}"
    
    def _process_messages(self, messages: List[Dict[str, Any]]):
        """Process and add messages to chat history"""
        # Start a new conversation for imported data
        self.chat_history.start_new_conversation()
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role in ['user', 'assistant'] and content:
                self.chat_history.add_message(role, content)
    
    def get_supported_formats(self) -> str:
        """Get information about supported import formats"""
        return """
📁 Supported Import Formats:

1. JSON Files:
   - List format: [{"role": "user", "content": "...", "timestamp": "..."}]
   - Conversations format: {"conversations": [[messages], [messages]]}
   - Messages format: {"messages": [{"role": "...", "content": "..."}]}

2. CSV Files:
   - Columns: role, content, timestamp (optional)
   - Example: role,content,timestamp
            user,Hello,2024-01-15T10:00:00
            assistant,Hi there!,2024-01-15T10:00:01

3. Text Files:
   - Format: "Speaker: message"
   - Example: User: Hello
            Assistant: Hi there!

4. Manual Input:
   - Provide conversation data directly in code
""" 