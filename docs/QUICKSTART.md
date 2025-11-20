# Quick Start Guide

**⏱️ Time Estimate: 5-10 minutes**

Get TrendRadar up and running with the fastest deployment method (GitHub Actions).

## Table of Contents
- [Overview](#overview)
- [What You'll Need](#what-youll-need)
- [Quick Setup Steps](#quick-setup-steps)
- [First Notification Test](#first-notification-test)
- [What's Next](#whats-next)

## Overview

**TrendRadar** is an AI-powered news aggregation and trend analysis tool that helps you stay informed without information overload.

### What TrendRadar Does:
- 📰 **Tracks 35+ News Platforms**: Monitors Chinese news sources (Zhihu, Weibo, Baidu, etc.) and USA financial markets (Yahoo Finance, MarketWatch, etc.)
- 🎯 **Personalized Filtering**: Only sends you news matching your custom keywords
- 📱 **Multi-Channel Notifications**: Delivers updates via Email or ntfy
- 🤖 **AI Analysis**: Provides conversational trend analysis through MCP integration
- ☁️ **Zero-Maintenance Deployment**: Runs automatically on GitHub Actions (no server needed)

### Perfect For:
- 📈 Investors tracking market trends
- 📝 Content creators finding hot topics
- 🔍 Researchers monitoring specific subjects
- 📊 PR professionals tracking brand mentions
- 🌐 Anyone wanting curated news instead of algorithm feeds

## What You'll Need

✅ A GitHub account (free)  
✅ 5-10 minutes of your time  
✅ One notification channel set up (we recommend starting with ntfy for simplicity or Email for reliability)

**No programming knowledge required!**

## Quick Setup Steps

### Step 1: Fork the Repository (1 minute)

1. Go to [TrendRadar GitHub Repository](https://github.com/sansan0/TrendRadar)
2. Click the **"Fork"** button at the top right
3. Wait for GitHub to create your copy

✅ **What you should see**: Your own copy of TrendRadar at `github.com/YOUR-USERNAME/TrendRadar`

---

### Step 2: Choose Your Notification Channel (2 minutes)

Pick **one** notification method to start with (you can add more later):

<details>
<summary><b>Option A: ntfy (Recommended for Beginners)</b></summary>

**Why ntfy?** Open-source, self-hostable, no account needed, simple setup.

1. Download ntfy app: [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) | [iOS](https://apps.apple.com/us/app/ntfy/id1625396347)
2. Choose a unique topic name (e.g., `trendradar-yourname-8492`)
3. Subscribe to that topic in the app

**Save this for Step 3:**
- Topic name: `trendradar-yourname-8492`

</details>

<details>
<summary><b>Option B: Email (Most Reliable)</b></summary>

**Why Email?** Works everywhere, familiar, reliable delivery.

1. Use an existing email account (Gmail, Outlook, etc.)
2. For Gmail: Generate an App Password (Account → Security → 2-Step Verification → App passwords)
3. For other providers: Use your regular email password or app-specific password

**Save these for Step 3:**
- Sender Email: `your-email@gmail.com`
- Email Password/App Password: `your-app-password`
- Recipient Email: `recipient@example.com` (can be same as sender)

</details>

📖 **More Options**: See [CONFIGURATION.md](CONFIGURATION.md) for detailed Email setup instructions.

---

### Step 3: Configure GitHub Secrets (3 minutes)

GitHub Secrets keep your credentials secure and private.

1. In **your forked repository**, go to: **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add your notification credentials:

**For ntfy:**
| Name (exact) | Secret (value) |
|-------------|----------------|
| `NTFY_TOPIC` | Your topic name |

**For Email:**
| Name (exact) | Secret (value) |
|-------------|----------------|
| `EMAIL_FROM` | Sender email address |
| `EMAIL_PASSWORD` | Email password or app password |
| `EMAIL_TO` | Recipient email address |

⚠️ **Important**: 
- Copy the Name **exactly** as shown (case-sensitive)
- Click "Add secret" after each entry
- You won't see the Secret value after saving (this is normal)

✅ **What you should see**: Your secrets listed by name (values hidden)

---

### Step 4: Enable GitHub Actions (1 minute)

1. In your repository, click the **"Actions"** tab
2. If you see a prompt, click **"I understand my workflows, go ahead and enable them"**
3. Find **"Hot News Crawler"** in the workflows list

✅ **What you should see**: The Actions tab is active and workflows are enabled

---

## First Notification Test

### Run Your First Test (2 minutes)

1. In the **Actions** tab, click **"Hot News Crawler"**
2. Click **"Run workflow"** → **"Run workflow"** (green button)
3. Wait about 60 seconds

✅ **What you should see**: 
- A yellow dot turns into a green checkmark (workflow succeeded)
- A notification on your chosen platform (Email or ntfy)

### 🎉 Success! What's in Your First Notification?

Your first notification will show:
- 📊 Top trending news from 35+ platforms
- 🔥 Keywords matching the default configuration
- 🆕 New trending topics marked
- ⏰ Timestamp of the update

**Example notification content:**
```
🔥 Trending Keywords Stats

📱 [1/3] AI ChatGPT : 2 items
  1. [Baidu] ChatGPT-5 officially launched [1] - 09:15
  2. [Toutiao] AI chip stocks surge [3] - 08:30 ~ 10:45

Updated: 2025-01-15 12:30:15
```

---

## Troubleshooting Quick Fixes

### ❌ No notification received?

**Check 1**: Verify secrets are configured correctly
- Go to Settings → Secrets → Actions
- Confirm secret Names match exactly (case-sensitive)

**Check 2**: Verify workflow succeeded
- Actions tab → Check for green checkmark
- If red X, click it to see error logs

**Check 3**: Check notification settings
- Edit `config/config.yaml` in your fork
- Ensure `enable_notification: true`

📖 **More Help**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions

---

## What's Next?

Now that TrendRadar is running, customize it for your needs:

### 🎯 Customize Your Keywords (5 minutes)
- Edit `config/frequency_words.txt` in your repository
- Add topics you care about (e.g., `Bitcoin`, `Tesla`, `AI`)
- Remove default keywords you don't need
- 📖 **Learn more**: [Keyword Configuration Guide](CONFIGURATION.md#keyword-configuration)

### ⚙️ Adjust Push Settings (5 minutes)
- Choose between 3 push modes: `daily`, `current`, or `incremental`
- Set push time windows to avoid night-time notifications
- 📖 **Learn more**: [Push Mode Configuration](CONFIGURATION.md#report-mode)

### 🌐 Enable Web Dashboard (2 minutes)
- Go to Settings → Pages
- Select **"Deploy from a branch"** → **main** branch
- Get a beautiful web interface at `YOUR-USERNAME.github.io/TrendRadar`
- 📖 **Learn more**: [DEPLOYMENT.md](DEPLOYMENT.md#github-pages)

### 📱 Set Up Alternative Notification Channel (10 minutes)
- Set up both Email and ntfy for redundancy
- 📖 **Learn more**: [Notification Channels Setup](CONFIGURATION.md#notification-channels-setup)

### 🐳 Deploy on Your Server (15 minutes)
- Run TrendRadar on Docker for more control
- Customize execution schedules (every 10 minutes, hourly, etc.)
- 📖 **Learn more**: [Docker Deployment Guide](DEPLOYMENT.md#docker-deployment)

### 🤖 Enable AI Analysis (20 minutes)
- Query trends with natural language: "Show me AI news from yesterday"
- Get AI-powered insights and summaries
- 📖 **Learn more**: [README-Cherry-Studio.md](../README-Cherry-Studio.md)

---

## Getting Help

### 📚 Documentation
- **[Installation Guide](INSTALLATION.md)** - Detailed setup for all methods
- **[Configuration Guide](CONFIGURATION.md)** - Complete configuration reference
- **[Deployment Guide](DEPLOYMENT.md)** - Advanced deployment options
- **[Troubleshooting](TROUBLESHOOTING.md)** - Solutions to common problems

### 💬 Community Support
- **GitHub Issues**: [Report bugs or request features](https://github.com/sansan0/TrendRadar/issues)
- **Discussions**: [Ask questions and share tips](https://github.com/sansan0/TrendRadar/discussions)

### ⭐ Support the Project
If TrendRadar helps you stay informed, consider:
- ⭐ **Star the repository** on GitHub
- 📢 **Share** with others who might find it useful
- 🐛 **Report bugs** to help improve the project

---

**🎉 Congratulations!** You've successfully deployed TrendRadar and received your first personalized news update. Enjoy staying informed without information overload!

[← Back to README](../README-EN.md) | [Next: Full Installation Guide →](INSTALLATION.md)
