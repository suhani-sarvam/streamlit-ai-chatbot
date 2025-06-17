# Sarvam AI Chatbot

A simple and elegant chatbot built with Streamlit and powered by Sarvam AI's language models.

## Features

- 🤖 Real-time chat interface
- 💬 Conversation history
- 🎨 Clean and modern UI
- 📚 Wikipedia grounding support
- 🗑️ Clear conversation functionality
- 🔐 Secure API key handling

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   - Create a `.env` file in the project root
   - Add your Sarvam AI API key: `SARVAM_API_KEY=your_api_key_here`

3. **Run the chatbot:**
   ```bash
   streamlit run chatbot.py
   ```

4. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## Usage

- Type your message in the chat input at the bottom
- Press Enter to get a response from the AI
- Use the sidebar to:
  - Adjust reasoning effort (low/medium/high)
  - Enable Wikipedia grounding for factual queries
  - Clear conversation history
- The conversation history is maintained throughout your session

## Deployment

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

## Dependencies

- `streamlit`: Web app framework
- `sarvamai`: Sarvam AI Python SDK
- `requests`: HTTP requests
- `python-dotenv`: Environment variable management

## Security

- API keys are stored securely in environment variables
- `.env` file is gitignored to prevent accidental commits
- Use Streamlit secrets for cloud deployment

## Troubleshooting

If you encounter any issues:
1. Make sure all dependencies are installed correctly
2. Check that your API key is properly set in the `.env` file
3. Verify your internet connection
4. Check the terminal for error messages

Enjoy chatting with your AI assistant! 🚀
