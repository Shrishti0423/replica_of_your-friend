#!/usr/bin/env python3
"""
Example: How to import your custom chat data
"""

from ai_chatbot import AIChatbot

def main():
    # Initialize chatbot
    chatbot = AIChatbot()
    
    # YOUR CUSTOM CHAT DATA HERE
    # Replace this with your actual conversation data
    your_conversation = [
        {"role": "user", "content": "Hi, my name is [Your Name]"},
        {"role": "assistant", "content": "Hello [Your Name]! How can I help you today?"},
        {"role": "user", "content": "I work as a [Your Job] and I'm interested in [Your Interest]"},
        {"role": "assistant", "content": "That's fascinating! Tell me more about your work in [Your Job]."},
        # Add more messages from your conversation...
    ]
    
    # Import your conversation
    result = chatbot.import_manual_conversation(your_conversation)
    print(f"Import result: {result}")
    
    # Now start chatting - the AI will remember your context
    print("\n🤖 Chatbot is ready with your conversation context!")
    print("You can now ask questions and the AI will remember your details.")
    
    # Example: Ask about yourself
    response = chatbot.generate_response("What's my name and what do I do?")
    print(f"AI: {response}")

if __name__ == "__main__":
    main() 