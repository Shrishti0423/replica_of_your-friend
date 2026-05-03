#!/usr/bin/env python3
"""
Sapna Chatbot - Terminal Interface
Chat with an AI that acts like Sapna based on chat analysis
"""

import sys
import os
from colorama import init, Fore, Style
from sapna_chatbot import SapnaChatbot

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_banner():
    """Print the Sapna chatbot banner"""
    banner = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}SAPNA CHATBOT{Fore.MAGENTA}                        ║
║              {Fore.GREEN}AI that acts like Sapna{Fore.MAGENTA}                    ║
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
{Fore.GREEN}/quit{Style.RESET_ALL}     - Exit the chatbot
{Fore.GREEN}/clear{Style.RESET_ALL}    - Clear the screen

{Fore.YELLOW}About Sapna:{Style.RESET_ALL}
- Speaks in Hinglish (Hindi + English)
- Uses "Kaku" to address you
- Loves food (momos, kurkure, safle)
- Direct and sometimes demanding but caring
- Student interested in medical field

{Fore.YELLOW}Usage:{Style.RESET_ALL}
Just type your message and press Enter to chat with Sapna!
"""
    print(help_text)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main Sapna chatbot interface"""
    print_banner()
    
    # Check if API key is configured
    if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
        print(f"{Fore.RED}⚠️  Warning: OpenAI API key not configured!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set your OpenAI API key in the config.py file or as an environment variable.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}You can get an API key from: https://platform.openai.com/api-keys{Style.RESET_ALL}")
        print()
    
    # Initialize Sapna chatbot
    try:
        sapna = SapnaChatbot()
        print(f"{Fore.GREEN}✅ Sapna chatbot initialized successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to initialize Sapna chatbot: {e}{Style.RESET_ALL}")
        return
    
    print_help()
    print(f"{Fore.MAGENTA}💬 Start chatting with Sapna (type /help for commands):{Style.RESET_ALL}")
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
                command = user_input.lower()
                
                if command == '/quit' or command == '/exit':
                    print(f"{Fore.YELLOW}👋 Bye! Sapna says goodbye!{Style.RESET_ALL}")
                    break
                elif command == '/help':
                    print_help()
                    continue
                elif command == '/new':
                    result = sapna.start_new_conversation()
                    print(f"{Fore.MAGENTA}💬 {result}{Style.RESET_ALL}")
                    continue
                elif command == '/history':
                    summary = sapna.get_conversation_summary()
                    print(f"{Fore.MAGENTA}📜 {summary}{Style.RESET_ALL}")
                    continue
                elif command == '/clear':
                    clear_screen()
                    print_banner()
                    continue
                else:
                    print(f"{Fore.RED}❌ Unknown command: {user_input}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Type /help for available commands{Style.RESET_ALL}")
                    continue
            
            # Generate Sapna's response
            print(f"{Fore.MAGENTA}💭 Sapna is typing...{Style.RESET_ALL}")
            response = sapna.generate_sapna_response(user_input)
            
            # Print Sapna's response
            print(f"{Fore.MAGENTA}Sapna: {Style.RESET_ALL}{response}")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Bye! Sapna says goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
            continue

if __name__ == "__main__":
    main() 