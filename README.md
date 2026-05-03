# AI Chatbot with Memory

A terminal-based AI chatbot that analyzes previous chat conversations to provide contextual responses. Built with Python and OpenAI's GPT models.

## Features

- 🤖 **AI-Powered Responses**: Uses OpenAI's GPT models for intelligent conversations
- 🧠 **Memory & Context**: Remembers and analyzes previous chat history
- 💾 **Persistent Storage**: Saves conversations to JSON files
- 🎨 **Beautiful Terminal UI**: Colored output with emojis and formatting
- ⚡ **Command System**: Built-in commands for conversation management
- 🔧 **Configurable**: Easy to customize settings and API configuration

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and get your API key
3. Set the API key in one of these ways:

**Option A: Environment Variable**
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

**Option B: Edit config.py**
```python
OPENAI_API_KEY = 'your_api_key_here'
```

### 3. Run the Chatbot

```bash
python main.py
```

## Usage

### Basic Chatting
Just type your message and press Enter. The AI will respond based on the conversation context.

### Available Commands

- `/help` - Show help information
- `/new` - Start a new conversation (clears current context)
- `/history` - Show conversation history summary
- `/clear` - Clear the terminal screen
- `/quit` - Exit the chatbot

### Example Conversation

```
You: Hi, my name is John
AI: Hello John! Nice to meet you. How can I help you today?

You: I'm working on a Python project
AI: That's great, John! Python is a fantastic language for development. 
    What kind of project are you working on? I'd be happy to help with 
    any questions you might have about Python programming.

You: It's a web application using Flask
AI: Excellent choice, John! Flask is a lightweight and flexible web 
    framework for Python. Are you building a specific type of web 
    application? I can help you with Flask routing, templates, 
    database integration, or any other aspects of your project.
```

## Project Structure

```
chatbot/
├── main.py              # Main terminal interface
├── ai_chatbot.py        # AI chatbot logic
├── chat_history.py      # Chat history management
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── chat_history.json  # Stored conversations (created automatically)
```

## Configuration

Edit `config.py` to customize:

- **Model**: Change `MODEL_NAME` (default: 'gpt-3.5-turbo')
- **Temperature**: Adjust `TEMPERATURE` (0.0-1.0, default: 0.7)
- **History Length**: Modify `MAX_HISTORY` (default: 10 exchanges)
- **Storage**: Change `CHAT_HISTORY_FILE` location

## How It Works

1. **Message Storage**: Each user message and AI response is stored with timestamps
2. **Context Analysis**: When generating responses, the AI receives the full conversation history
3. **Memory Management**: Automatically limits history length to prevent token overflow
4. **Persistent Storage**: Conversations are saved to JSON files and restored on restart

## Troubleshooting

### Common Issues

**"Invalid API key" error**
- Check your OpenAI API key is correct
- Ensure you have sufficient API credits

**"Rate limit exceeded" error**
- Wait a moment and try again
- Consider upgrading your OpenAI plan

**Import errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### Getting Help

If you encounter issues:
1. Check the error messages in the terminal
2. Verify your API key is set correctly
3. Ensure all dependencies are installed
4. Check your internet connection

## Advanced Usage

### Custom System Prompts

Edit the system message in `ai_chatbot.py` to change the AI's personality:

```python
system_message = {
    'role': 'system',
    'content': 'You are a helpful coding assistant. Focus on programming questions and provide code examples.'
}
```

### Multiple Conversations

The chatbot supports multiple conversation sessions. Use `/new` to start fresh conversations while keeping old ones in the history file.

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chatbot! 