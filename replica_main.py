#!/usr/bin/env python3
"""
Generic Chat Replica - Terminal Interface
Create AI replicas of anyone by uploading their chat history
"""

import sys
import os
from colorama import init, Fore, Style
from generic_chat_replica import GenericChatReplica

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the replica chatbot banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║              {Fore.YELLOW}GENERIC CHAT REPLICA CREATOR{Fore.CYAN}                   ║
║        {Fore.GREEN}Create AI that acts like anyone{Fore.CYAN}                   ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

def print_help():
    """Print help information"""
    help_text = f"""
{Fore.YELLOW}Available Commands:{Style.RESET_ALL}
{Fore.GREEN}/help{Style.RESET_ALL}     - Show this help message
{Fore.GREEN}/create{Style.RESET_ALL}   - Create a new replica (interactive setup)
{Fore.GREEN}/profile{Style.RESET_ALL}  - Show current person's profile
{Fore.GREEN}/new{Style.RESET_ALL}      - Start new conversation with replica
{Fore.GREEN}/history{Style.RESET_ALL}  - Show conversation history
{Fore.GREEN}/clear{Style.RESET_ALL}    - Clear screen
{Fore.GREEN}/quit{Style.RESET_ALL}     - Exit

{Fore.YELLOW}How to Use:{Style.RESET_ALL}
1. Use {Fore.GREEN}/create{Style.RESET_ALL} to set up a replica
2. Upload a chat file (JSON, CSV, or TXT)
3. Chat with the AI replica of that person
4. The AI will mimic their personality, style, and tone

{Fore.YELLOW}Supported Formats:{Style.RESET_ALL}
- JSON: {{"role": "user", "content": "..."}}
- CSV: role, content, timestamp
- Text: User: message
"""
    print(help_text)

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_replica(replica):
    """Interactive setup for creating a new replica"""
    print(f"\n{Fore.CYAN}=== CREATE NEW REPLICA ==={Style.RESET_ALL}")
    
    # Get person name
    person_name = input(f"{Fore.YELLOW}Enter the person's name: {Style.RESET_ALL}").strip()
    if not person_name:
        print(f"{Fore.RED}Name cannot be empty!{Style.RESET_ALL}")
        return
    
    # Get file path
    file_path = input(f"{Fore.YELLOW}Enter the chat file path (JSON/CSV/TXT): {Style.RESET_ALL}").strip()
    if not os.path.exists(file_path):
        print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
        return
    
    # Get file format
    print(f"{Fore.CYAN}Supported formats: json, csv, text{Style.RESET_ALL}")
    file_format = input(f"{Fore.YELLOW}Enter file format: {Style.RESET_ALL}").strip().lower()
    
    if file_format not in ['json', 'csv', 'text']:
        print(f"{Fore.RED}Unsupported format: {file_format}{Style.RESET_ALL}")
        return
    
    # Create replica
    print(f"{Fore.YELLOW}Creating replica for {person_name}...{Style.RESET_ALL}")
    result = replica.create_replica_from_file(file_path, file_format, person_name)
    print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")

def main():
    """Main terminal interface"""
    print_banner()
    
    # Check API key
    if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
        print(f"{Fore.RED}Warning: OpenAI API key not configured!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Set it in config.py or as environment variable{Style.RESET_ALL}\n")
    
    # Initialize replica
    try:
        replica = GenericChatReplica()
        print(f"{Fore.GREEN}Ready to create chat replicas!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return
    
    print_help()
    print(f"{Fore.CYAN}Start by using {Fore.GREEN}/create{Fore.CYAN} to set up a replica:{Style.RESET_ALL}")
    print("-" * 60)
    
    # Main loop
    while True:
        try:
            user_input = input(f"{Fore.BLUE}You: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command = user_input.lower()
                
                if command == '/quit' or command == '/exit':
                    print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                    break
                elif command == '/help':
                    print_help()
                    continue
                elif command == '/create':
                    setup_replica(replica)
                    continue
                elif command == '/profile':
                    if not replica.person_profile:
                        print(f"{Fore.YELLOW}No profile created yet. Use /create{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.MAGENTA}{replica.get_profile_summary()}{Style.RESET_ALL}")
                    continue
                elif command == '/new':
                    result = replica.start_new_conversation()
                    print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
                    continue
                elif command == '/history':
                    summary = replica.get_conversation_summary()
                    print(f"{Fore.MAGENTA}{summary}{Style.RESET_ALL}")
                    continue
                elif command == '/clear':
                    clear_screen()
                    print_banner()
                    continue
                else:
                    print(f"{Fore.RED}Unknown command{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Type /help for commands{Style.RESET_ALL}")
                    continue
            
            # Generate response
            if not replica.person_profile:
                print(f"{Fore.RED}Error: No replica created. Use /create first{Style.RESET_ALL}")
                continue
            
            print(f"{Fore.YELLOW}Generating response...{Style.RESET_ALL}")
            response = replica.generate_response(user_input)
            
            person_name = replica.person_name
            print(f"{Fore.MAGENTA}{person_name}: {Style.RESET_ALL}{response}")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            continue

if __name__ == "__main__":
    main()
