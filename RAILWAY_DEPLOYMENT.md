# 🚀 Railway Deployment Guide

Complete guide to deploy your Instagram Carousel Generator to Railway.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Push your code to GitHub
3. **API Key**: DeepSeek API key ready

---

## 🔧 Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Railway deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/instagram-feeds-generator.git
git branch -M main
git push -u origin main
```

---

## 🚂 Step 2: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. Go to [railway.app](https://railway.app) and log in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `instagram-feeds-generator` repository
5. Railway will automatically detect your configuration

### Option B: Deploy from CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

---

## 🔑 Step 3: Set Environment Variables

In Railway dashboard:

1. Click on your project
2. Go to **Variables** tab
3. Add these variables:

```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

---

## ⚙️ Step 4: Configure Build Settings

Railway should auto-detect from `railway.toml`, but verify:

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
```

**Start Command:**
```bash
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

---

## 📦 Step 5: Add Persistent Storage (Optional)

For caching scraped images across deployments:

1. In Railway dashboard, click **"New"** → **"Volume"**
2. Mount path: `/app/output`
3. This keeps cached images even after restarts

---

## ✅ Step 6: Verify Deployment

1. Wait for build to complete (~5-10 minutes first time)
2. Railway will provide a URL like: `https://your-app.railway.app`
3. Open the URL and test carousel generation
4. Check logs in Railway dashboard if issues occur

---

## 🔍 Troubleshooting

### Playwright Issues

If Chromium fails to install:

```toml
# Already configured in railway.toml
[build]
buildCommand = "pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium"
```

### Memory Issues

If app crashes due to memory:

1. In Railway dashboard → **Settings** → **Resources**
2. Upgrade to Hobby plan ($5/month) for more memory

### Port Issues

Ensure your app uses `$PORT` environment variable (already configured in `Procfile`).

---

## 💰 Pricing

- **Free Tier**: $5 credit/month (~500 hours)
- **Hobby Plan**: $5/month for more resources
- **Pro Plan**: $20/month for production apps

**Estimated Usage:**
- Small traffic: Free tier sufficient
- Medium traffic: Hobby plan recommended
- High traffic: Pro plan recommended

---

## 🎯 Post-Deployment Checklist

- [ ] App accessible via Railway URL
- [ ] Environment variables set correctly
- [ ] Carousel generation works
- [ ] AI image scraping functional
- [ ] Playwright rendering working
- [ ] Check Railway logs for errors

---

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Streamlit Deployment: https://docs.streamlit.io/knowledge-base/tutorials/deploy

---

## 🆘 Support

If deployment fails:

1. Check Railway logs: `railway logs`
2. Verify environment variables are set
3. Check build logs for Playwright installation errors
4. Try rebuilding: Railway Dashboard → **Settings** → **Redeploy**

---

## 🎉 Success!

Once deployed, your app will be:
- ✅ Available 24/7
- ✅ Faster image scraping
- ✅ Better Playwright performance
- ✅ Professional cloud hosting

Share your Railway URL with users! 🚀
