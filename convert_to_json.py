#!/usr/bin/env python3
"""
Chat to JSON Converter
Convert your chat exports to JSON format for the replica system
"""

import json
import os
import re
from datetime import datetime

def convert_whatsapp_to_json(input_file, person_name, output_file=None):
    """
    Convert WhatsApp export (.txt) to JSON
    
    Args:
        input_file: Path to WhatsApp export file
        person_name: Name of the person to replicate
        output_file: Output JSON file (default: same name as input)
    
    Returns:
        List of messages in JSON format
    """
    messages = []
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        return None
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip system messages
            if 'Messages and calls are encrypted' in line:
                continue
            if 'You created this group' in line:
                continue
            if 'was added' in line or 'was removed' in line:
                continue
            
            # Parse: [timestamp] Name: message
            try:
                # Remove timestamp [HH:MM, DD/MM/YYYY or similar]
                if line.startswith('['):
                    # Find the ] that closes timestamp
                    end_bracket = line.find(']')
                    if end_bracket != -1:
                        line = line[end_bracket + 2:]  # Skip '] '
                
                # Split name and message
                if ': ' not in line:
                    continue
                
                name, message = line.split(': ', 1)
                name = name.strip()
                message = message.strip()
                
                if not name or not message:
                    continue
                
                # Determine role
                if name == person_name:
                    role = 'user'
                else:
                    role = 'assistant'
                
                messages.append({
                    'role': role,
                    'content': message
                })
            except:
                continue
        
        if not output_file:
            output_file = input_file.rsplit('.', 1)[0] + '.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        
        print(f"Success! Converted {len(messages)} messages")
        print(f"Output: {output_file}")
        return messages
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_plain_text_to_json(input_file, user_name='User', assistant_name='Assistant', output_file=None):
    """
    Convert plain text format to JSON
    Format: Name: message
    
    Args:
        input_file: Path to text file
        user_name: Name of the person being replicated
        assistant_name: Name of responses (can be anything)
        output_file: Output JSON file
    
    Returns:
        List of messages
    """
    messages = []
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        return None
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            try:
                if ': ' not in line:
                    continue
                
                name, message = line.split(': ', 1)
                name = name.strip()
                message = message.strip()
                
                if not name or not message:
                    continue
                
                # Determine role
                if name.lower() == user_name.lower():
                    role = 'user'
                else:
                    role = 'assistant'
                
                messages.append({
                    'role': role,
                    'content': message
                })
            except:
                continue
        
        if not output_file:
            output_file = input_file.rsplit('.', 1)[0] + '.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        
        print(f"Success! Converted {len(messages)} messages")
        print(f"Output: {output_file}")
        return messages
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def interactive_converter():
    """Interactive converter - ask user for details"""
    print("\n" + "="*60)
    print("CHAT TO JSON CONVERTER")
    print("="*60)
    
    print("\nWhat type of chat are you converting?")
    print("1. WhatsApp export (.txt)")
    print("2. Plain text (Name: message format)")
    print("3. Already in JSON (just verify)")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        file_path = input("Enter path to WhatsApp file (e.g., chat.txt): ").strip()
        person_name = input("Enter the person's name (as it appears in chat): ").strip()
        
        if file_path and person_name:
            convert_whatsapp_to_json(file_path, person_name)
    
    elif choice == '2':
        file_path = input("Enter path to text file (e.g., chat.txt): ").strip()
        user_name = input("Enter the person's name: ").strip()
        
        if file_path and user_name:
            convert_plain_text_to_json(file_path, user_name, 'Other')
    
    elif choice == '3':
        file_path = input("Enter path to JSON file: ").strip()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"JSON is valid! Contains {len(data)} messages")
            except:
                print("JSON format is invalid. Please check the file.")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        interactive_converter()
    
    elif len(sys.argv) >= 2:
        file_path = sys.argv[1]
        file_type = sys.argv[2].lower() if len(sys.argv) > 2 else 'whatsapp'
        person_name = sys.argv[3] if len(sys.argv) > 3 else input("Enter person's name: ")
        
        if file_type == 'whatsapp':
            convert_whatsapp_to_json(file_path, person_name)
        else:
            convert_plain_text_to_json(file_path, person_name)
    
    print("\nNext: Use with replica system")
    print("  python replica_main.py")
    print("  /create")
    print("  Upload your chat.json file")
