# Deployment Checklist for Streamlit Cloud

Use this checklist to ensure your app is ready for deployment.

## ✅ Pre-Deployment Checklist

### 1. Code & Repository
- [x] All code committed to GitHub
- [x] `.gitignore` includes `.streamlit/secrets.toml`
- [x] `.gitignore` includes `.env` and sensitive files
- [x] `requirements.txt` is complete and up-to-date
- [x] README.md has clear instructions

### 2. API Keys & Security
- [ ] Obtained Google Gemini API key
- [ ] Obtained Data.gov.in API key
- [ ] Tested both API keys work locally
- [ ] Created `.streamlit/secrets.toml` locally (for testing)
- [ ] Verified `.streamlit/secrets.toml` is in `.gitignore`

### 3. Local Testing
- [ ] Run `pip install -r requirements.txt`
- [ ] Add API keys to `.streamlit/secrets.toml`
- [ ] Run `streamlit run streamlit_app_direct.py`
- [ ] Test with query: "average annual rainfall in 1951 in Odisha"
- [ ] Verify conversational response is generated
- [ ] Check data sources are properly attributed

## 🚀 Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `streamlit_app_direct.py`
6. Click "Deploy"

### Step 3: Add Secrets
In Streamlit Cloud dashboard:
1. Go to app settings
2. Click "Secrets" in sidebar
3. Add this content:
```toml
GEMINI_API_KEY = "your-actual-gemini-key-here"
DATA_GOV_API_KEY = "your-actual-data-gov-key-here"
```
4. Click "Save"

### Step 4: Verify Deployment
- [ ] App starts without errors
- [ ] Test query works
- [ ] Conversational response generated
- [ ] No API key errors in logs

## 🔧 Troubleshooting

### App won't start
- Check logs in Streamlit Cloud dashboard
- Verify all packages in `requirements.txt` are valid
- Ensure Python version compatibility

### "Invalid API key" error
- Double-check keys in Secrets (no extra spaces)
- Verify keys work on provider's website
- Ensure correct format in secrets.toml

### "Module not found" error
- Add missing package to `requirements.txt`
- Push changes to GitHub
- Streamlit Cloud will auto-redeploy

### Slow performance
- Normal for first run (cold start)
- Cache builds up over time
- Consider Streamlit Cloud paid tier for better performance

## 📊 Post-Deployment

### Monitoring
- [ ] Check app logs regularly
- [ ] Monitor API usage/costs
- [ ] Watch for errors or crashes

### Usage Tracking
- [ ] Set up Google Analytics (optional)
- [ ] Track popular queries
- [ ] Monitor response times

### Updates
- Push to GitHub → Auto-deploys
- Test locally before pushing
- Monitor logs after deployment

## 🔐 Security Notes

### ✅ Secure Practices
- API keys stored in Streamlit Secrets (encrypted)
- `.streamlit/secrets.toml` in `.gitignore`
- No hardcoded credentials in code
- Environment variables used properly

### ❌ Don't Do This
- Never commit API keys to GitHub
- Don't hardcode secrets in code
- Don't share your secrets.toml file
- Don't expose API keys in logs

## 📝 Quick Reference

### Streamlit Cloud URLs
- Dashboard: [share.streamlit.io](https://share.streamlit.io)
- Docs: [docs.streamlit.io](https://docs.streamlit.io)
- Community: [discuss.streamlit.io](https://discuss.streamlit.io)

### API Key Sources
- Gemini: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- Data.gov.in: [data.gov.in](https://data.gov.in/)

### Your App
- Repository: `https://github.com/your-username/Samarth_app_claude`
- Deployed URL: `https://your-app-name.streamlit.app`
- Logs: Check in Streamlit Cloud dashboard

## ✨ Success Criteria

Your deployment is successful when:
- ✅ App loads without errors
- ✅ Can ask questions and get conversational responses
- ✅ Data sources properly attributed
- ✅ Historical state names work (Odisha/Orissa)
- ✅ No API key errors
- ✅ Response quality is high

---

**Need Help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
