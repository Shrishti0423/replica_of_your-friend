#!/usr/bin/env python3
"""
Simple test for Sapna chatbot
"""

try:
    from sapna_chatbot import SapnaChatbot
    print("✅ Successfully imported SapnaChatbot")
    
    # Test initialization
    sapna = SapnaChatbot()
    print("✅ Successfully created SapnaChatbot instance")
    
    # Test simple response
    response = sapna.generate_sapna_response("Hi")
    print(f"✅ Sapna responded: {response}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e)}") 