#!/usr/bin/env python3
"""
AI Chatbot with Chat History Analysis
Terminal-based chatbot that remembers and analyzes previous conversations
"""

import sys
import os
from colorama import init, Fore, Style
from ai_chatbot import AIChatbot

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_banner():
    """Print the chatbot banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}AI CHATBOT WITH MEMORY{Fore.CYAN}                    ║
║              {Fore.GREEN}Analyzes previous chats for context{Fore.CYAN}              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

def print_help():
    """Print help information"""
    help_text = f"""
{Fore.YELLOW}Available Commands:{Style.RESET_ALL}
{Fore.GREEN}/help{Style.RESET_ALL}     - Show this help message
{Fore.GREEN}/new{Style.RESET_ALL}      - Start a new conversation
{Fore.GREEN}/history{Style.RESET_ALL}  - Show conversation history
{Fore.GREEN}/import{Style.RESET_ALL}   - Import chat data from file
{Fore.GREEN}/formats{Style.RESET_ALL}  - Show supported import formats
{Fore.GREEN}/quit{Style.RESET_ALL}     - Exit the chatbot
{Fore.GREEN}/clear{Style.RESET_ALL}    - Clear the screen

{Fore.YELLOW}Usage:{Style.RESET_ALL}
Just type your message and press Enter to chat with the AI.
The bot will remember your conversation and provide contextual responses.

{Fore.YELLOW}Import Usage:{Style.RESET_ALL}
/import json filename.json    - Import from JSON file
/import csv filename.csv      - Import from CSV file  
/import text filename.txt     - Import from text file
"""
    print(help_text)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_import_command(chatbot, command_parts):
    """Handle import commands"""
    if len(command_parts) < 3:
        print(f"{Fore.RED}❌ Usage: /import <format> <filename>{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Example: /import json my_chat.json{Style.RESET_ALL}")
        return
    
    format_type = command_parts[1].lower()
    file_path = command_parts[2]
    
    if not os.path.exists(file_path):
        print(f"{Fore.RED}❌ File not found: {file_path}{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}📁 Importing from {file_path}...{Style.RESET_ALL}")
    
    if format_type == 'json':
        result = chatbot.import_chat_from_json(file_path)
    elif format_type == 'csv':
        result = chatbot.import_chat_from_csv(file_path)
    elif format_type == 'text':
        result = chatbot.import_chat_from_text(file_path)
    else:
        print(f"{Fore.RED}❌ Unsupported format: {format_type}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Use /formats to see supported formats{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")

def main():
    """Main chatbot interface"""
    print_banner()
    
    # Check if API key is configured
    if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
        print(f"{Fore.RED}⚠️  Warning: OpenAI API key not configured!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set your OpenAI API key in the config.py file or as an environment variable.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}You can get an API key from: https://platform.openai.com/api-keys{Style.RESET_ALL}")
        print()
    
    # Initialize chatbot
    try:
        chatbot = AIChatbot()
        print(f"{Fore.GREEN}✅ Chatbot initialized successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to initialize chatbot: {e}{Style.RESET_ALL}")
        return
    
    print_help()
    print(f"{Fore.CYAN}Type your message or use /help for commands:{Style.RESET_ALL}")
    print("-" * 60)
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.BLUE}You: {Style.RESET_ALL}").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command_parts = user_input.split()
                command = command_parts[0].lower()
                
                if command == '/quit' or command == '/exit':
                    print(f"{Fore.YELLOW}👋 Goodbye! Thanks for chatting!{Style.RESET_ALL}")
                    break
                elif command == '/help':
                    print_help()
                    continue
                elif command == '/new':
                    result = chatbot.start_new_conversation()
                    print(f"{Fore.GREEN}🤖 {result}{Style.RESET_ALL}")
                    continue
                elif command == '/history':
                    summary = chatbot.get_conversation_summary()
                    print(f"{Fore.MAGENTA}📜 {summary}{Style.RESET_ALL}")
                    continue
                elif command == '/import':
                    handle_import_command(chatbot, command_parts)
                    continue
                elif command == '/formats':
                    formats = chatbot.get_import_formats()
                    print(f"{Fore.CYAN}{formats}{Style.RESET_ALL}")
                    continue
                elif command == '/clear':
                    clear_screen()
                    print_banner()
                    continue
                else:
                    print(f"{Fore.RED}❌ Unknown command: {user_input}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Type /help for available commands{Style.RESET_ALL}")
                    continue
            
            # Generate AI response
            print(f"{Fore.YELLOW}🤖 Thinking...{Style.RESET_ALL}")
            response = chatbot.generate_response(user_input)
            
            # Print AI response
            print(f"{Fore.GREEN}AI: {Style.RESET_ALL}{response}")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Goodbye! Thanks for chatting!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
            continue

if __name__ == "__main__":
    main() 