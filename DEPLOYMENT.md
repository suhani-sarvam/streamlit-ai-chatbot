# 🚀 Deployment Guide

## 1. GitHub Setup

### Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New Repository"
3. Name it `sarvam-ai-chatbot`
4. Make it **Public** (required for free Streamlit Cloud)
5. Don't initialize with README (we already have one)

### Connect Local Repository
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/sarvam-ai-chatbot.git
git push -u origin main
```

## 2. Streamlit Cloud Deployment

### Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/sarvam-ai-chatbot`
5. Branch: `main`
6. Main file path: `chatbot.py`
7. Click "Deploy"

### Add API Key to Streamlit Secrets
1. In your Streamlit Cloud app dashboard
2. Click "Settings" → "Secrets"
3. Add this content:
```toml
SARVAM_API_KEY = "0b74c0fe-aa1c-476f-aaf1-700741106598"
```
4. Click "Save"

## 3. Alternative: Local Development

### Run Locally
```bash
# Make sure you have the .env file with your API key
pip install -r requirements.txt
streamlit run chatbot.py
```

## 4. Environment Variables

### For Production
Set `SARVAM_API_KEY` in your deployment platform:
- **Streamlit Cloud**: Use Secrets management
- **Heroku**: `heroku config:set SARVAM_API_KEY=your_key`
- **Railway**: Add in Environment Variables
- **Vercel**: Add in Environment Variables

### Security Notes
- ✅ API key is stored securely in environment variables
- ✅ `.env` file is gitignored (not committed to GitHub)
- ✅ Use Streamlit secrets for cloud deployment
- ❌ Never hardcode API keys in your code

## 5. Troubleshooting

### Common Issues
1. **"API key not found"**: Check if `SARVAM_API_KEY` is set in secrets
2. **"Import error"**: Make sure `requirements.txt` includes all dependencies
3. **"Streamlit app won't start"**: Check logs in Streamlit Cloud dashboard

### Support
- [Streamlit Community](https://discuss.streamlit.io/)
- [Streamlit Docs](https://docs.streamlit.io/) 