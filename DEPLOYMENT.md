# Streamlit Cloud Deployment Guide

This guide will help you deploy the Samarth Agricultural Data Analysis app to Streamlit Cloud.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **API Keys**:
   - Google Gemini API Key: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Data.gov.in API Key: Get from [data.gov.in](https://data.gov.in/)

## Step 1: Prepare Your Repository

1. Make sure all your code is committed to GitHub
2. Verify `.gitignore` includes `.streamlit/secrets.toml` (already configured)
3. Ensure `requirements.txt` is up to date

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub repository
4. Configure deployment settings:
   - **Repository**: `your-username/Samarth_app_claude`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `streamlit_app_direct.py`
   - **App URL**: Choose a custom URL (e.g., `samarth-agriculture.streamlit.app`)

## Step 3: Add Secrets (API Keys)

**IMPORTANT**: This is how you keep your API keys secure!

1. In the Streamlit Cloud dashboard, go to your app settings
2. Click on **"Secrets"** in the left sidebar
3. Add your secrets in TOML format:

```toml
# Copy this format and paste in the Secrets section
GEMINI_API_KEY = "your-actual-gemini-api-key-here"
DATA_GOV_API_KEY = "your-actual-data-gov-api-key-here"
```

4. Click **"Save"**

**Security Notes**:
- ✅ Secrets are encrypted and never exposed in logs
- ✅ Secrets are only accessible to your app
- ✅ Never commit secrets to GitHub
- ✅ The `.gitignore` prevents accidental commits

## Step 4: Deploy

1. Click **"Deploy!"**
2. Wait for the app to build (2-3 minutes first time)
3. Your app will be live at your chosen URL!

## Step 5: Monitor and Manage

### View Logs
- Click "Manage app" → "Logs" to see real-time logs
- Useful for debugging if something goes wrong

### Update App
- Just push changes to GitHub
- Streamlit Cloud auto-deploys on every commit to main branch

### Restart App
- If needed: Settings → "Reboot app"

## Local Development with Secrets

For local testing, create a secrets file:

```bash
# Create secrets file (not tracked by git)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit and add your actual API keys
nano .streamlit/secrets.toml
```

Then run locally:
```bash
streamlit run streamlit_app_direct.py
```

## Troubleshooting

### App won't start
- Check logs for errors
- Verify `requirements.txt` has all dependencies
- Ensure API keys are correctly set in Secrets

### "Module not found" error
- Add missing package to `requirements.txt`
- Reboot the app

### "Invalid API key" error
- Double-check your API keys in Secrets
- Ensure no extra spaces or quotes
- Verify keys are valid on the provider's website

### Performance Issues
- Streamlit Cloud free tier has resource limits
- Consider upgrading if you need more resources
- Optimize data caching

## Resource Limits (Free Tier)

- **Memory**: 1 GB RAM
- **CPU**: Shared CPU
- **Storage**: 1 GB
- **Apps**: Unlimited public apps
- **Sleep**: Apps sleep after inactivity (auto-wake on visit)

## Sharing Your App

Once deployed, share your app URL:
```
https://your-app-name.streamlit.app
```

Anyone can access it without needing API keys - your secrets are secure!

## Support

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Issues**: Report bugs in your GitHub repository
