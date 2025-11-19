# Deployment Guide

**⏱️ Time Estimate: 10-30 minutes (depending on method)**

Complete deployment guide for all TrendRadar execution methods.

## Table of Contents
- [Deployment Overview](#deployment-overview)
- [GitHub Actions Deployment (Recommended)](#github-actions-deployment-recommended)
- [Docker Deployment](#docker-deployment)
- [Local Deployment](#local-deployment)
- [Comparison of Deployment Methods](#comparison-of-deployment-methods)
- [Next Steps](#next-steps)

---

## Deployment Overview

TrendRadar supports three deployment methods, each with different benefits:

| Method | Best For | Complexity | Cost | Updates |
|--------|----------|------------|------|---------|
| **GitHub Actions** | Beginners, zero maintenance | ⭐ Easy | Free | Automatic |
| **Docker** | NAS users, containerization fans | ⭐⭐ Medium | Free | Manual |
| **Local** | Developers, full control | ⭐⭐⭐ Advanced | Free | Manual |

**Choose based on your needs:**
- 🆕 **New users**: Start with GitHub Actions (simplest)
- 🏠 **NAS owners**: Use Docker (best for Synology/QNAP)
- 👨‍💻 **Developers**: Use Local (most flexible)

---

## GitHub Actions Deployment (Recommended)

**⏱️ Time: 10 minutes** | **Difficulty: Beginner** | **Free hosting on GitHub**

GitHub Actions runs TrendRadar automatically on GitHub's cloud servers. No server maintenance required!

### Prerequisites
- ✅ Completed [GitHub Fork installation](INSTALLATION.md#installation-method-1-github-fork-recommended)
- ✅ At least one notification channel configured

---

### Step 1: Enable GitHub Actions

If you haven't already enabled Actions during installation:

1. Go to your forked repository on GitHub
2. Click the **"Actions"** tab
3. Click **"I understand my workflows, go ahead and enable them"**

✅ **Verify**: You should see "Hot News Crawler" in the workflow list.

---

### Step 2: Configure GitHub Secrets

GitHub Secrets store your sensitive credentials securely.

#### Navigation
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**

#### Required Secrets (Choose at least one notification channel)

**⚠️ Important**: Secret names are **case-sensitive** and must match exactly!

##### Email Notification
| Secret Name | Description | Example |
|-------------|-------------|---------|
| `EMAIL_FROM` | Sender email address | `sender@gmail.com` |
| `EMAIL_PASSWORD` | Email password or auth code | `your-app-password` |
| `EMAIL_TO` | Recipient email(s), comma-separated | `receiver@example.com` |
| `EMAIL_SMTP_SERVER` | (Optional) SMTP server | `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | (Optional) SMTP port | `587` |

**Setup guide**: [Configuration - Email Notification](CONFIGURATION.md#email-notification)

---

##### ntfy Push
| Secret Name | Description | Example |
|-------------|-------------|---------|
| `NTFY_TOPIC` | Your unique topic name | `trendradar-yourname-8492` |
| `NTFY_SERVER_URL` | (Optional) Server URL | `https://ntfy.sh` |
| `NTFY_TOKEN` | (Optional) Access token | `tk_yourtoken` |

**Setup guide**: [Configuration - ntfy](CONFIGURATION.md#ntfy)

---

#### How to Add Secrets

For each secret:
1. Click **"New repository secret"**
2. Enter the **Name** (e.g., `EMAIL_FROM` or `NTFY_TOPIC`)
3. Enter the **Secret** value (your actual email/topic)
4. Click **"Add secret"**

**Screenshot reference location**: ![Adding Secret](images/add-secret.png)

✅ **Verify**: All required secrets appear in the secrets list (values are hidden for security)

---

### Step 3: Configure Workflow Schedule

The workflow file controls when and how often TrendRadar runs.

#### Edit Workflow File

1. In your repository, navigate to: `.github/workflows/crawler.yml`
2. Click the **pencil icon** (✏️) to edit
3. Find the `schedule` section (around line 5)

#### Schedule Configuration

```yaml
on:
  schedule:
    - cron: "0 * * * *"  # Every hour at minute 0
  workflow_dispatch:     # Allows manual triggering
```

#### Cron Schedule Examples

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Every hour | `0 * * * *` | Runs at :00 of each hour |
| Every 30 minutes | `*/30 * * * *` | Runs twice per hour |
| Every 2 hours | `0 */2 * * *` | Runs at 0:00, 2:00, 4:00... |
| Business hours only | `0 9-18 * * *` | Runs hourly from 9 AM to 6 PM |
| Twice daily | `0 9,21 * * *` | Runs at 9 AM and 9 PM |
| Every weekday | `0 9 * * 1-5` | Runs at 9 AM, Monday-Friday |

**Cron syntax**: `minute hour day month day-of-week`

⚠️ **GitHub Actions Limitations**:
- Schedules may have 3-10 minute delay due to queue
- Minimum recommended interval: 30 minutes (to avoid rate limits)
- Free tier: 2,000 minutes/month (enough for hourly runs)

**💡 Tip**: For precise scheduling, consider [Docker Deployment](#docker-deployment) on your own server.

#### Save Changes

After editing:
1. Scroll down and click **"Commit changes"**
2. Add commit message (e.g., "Update schedule to run every 30 minutes")
3. Click **"Commit changes"**

---

### Step 4: Verify Deployment

#### Manual Test Run

1. Go to **Actions** tab
2. Click **"Hot News Crawler"** workflow
3. Click **"Run workflow"** dropdown
4. Click green **"Run workflow"** button
5. Wait 1-2 minutes for execution

#### Check Execution Status

**During execution:**
- 🟡 Yellow dot = Running
- 🟢 Green checkmark = Success
- 🔴 Red X = Failed

**If successful:**
- ✅ Notification received on your device
- ✅ New files in `output/` folder
- ✅ Workflow shows green checkmark

**If failed:**
- Click the failed workflow run
- Check the logs for error messages
- See [Troubleshooting](#troubleshooting-github-actions) below

---

### Step 5: View Logs and Monitor

#### View Workflow Logs

1. Go to **Actions** tab
2. Click on any workflow run
3. Click **"crawl"** job
4. Expand sections to see detailed logs

**Key log sections:**
- **Setup Python**: Dependency installation
- **Run crawler**: Main execution with statistics
- **Commit and push**: Data persistence

#### Monitor Execution History

The Actions tab shows:
- ⏱️ Last run time
- ✅ Success rate
- 📊 Execution duration
- 📅 Schedule compliance

**Best practices:**
- Check logs after first few runs
- Monitor for any error patterns
- Adjust schedule if hitting rate limits

---

### Step 6: Enable GitHub Pages (Optional)

Get a beautiful web interface for your news reports!

1. Go to **Settings** → **Pages**
2. Under "Source", select **"Deploy from a branch"**
3. Select branch: **`main`** or **`master`**
4. Select folder: **`/ (root)`**
5. Click **"Save"**
6. Wait 1-2 minutes for deployment

✅ **Access your site**: `https://YOUR-USERNAME.github.io/TrendRadar/`

**Features:**
- 📱 Mobile-responsive design
- 💾 One-click save as image
- 🔗 Direct links to news sources
- 📊 Visual trend display

---

### Troubleshooting GitHub Actions

<details>
<summary>❌ Workflow not running automatically</summary>

**Possible causes:**
1. Actions not enabled → Enable in Actions tab
2. Schedule syntax error → Validate cron expression at [crontab.guru](https://crontab.guru/)
3. GitHub Actions outage → Check [GitHub Status](https://www.githubstatus.com/)
4. Repository is forked → Workflows in forks require manual trigger once

**Solution**: Manually trigger once, then automatic schedule will activate.
</details>

<details>
<summary>❌ No notifications received</summary>

**Check these:**
1. Verify secrets are set correctly (Settings → Secrets)
2. Check `config/config.yaml` has `enable_notification: true`
3. Review workflow logs for notification errors
4. Test webhook URLs manually (see Configuration guide)

**Debug command**: Add this to workflow for testing:
```yaml
- name: Test notification
  run: echo "Testing with EMAIL=${{ secrets.EMAIL_FROM }} TOPIC=${{ secrets.NTFY_TOPIC }}"
```
</details>

<details>
<summary>❌ Secrets not working</summary>

**Common mistakes:**
1. Secret name typo (case-sensitive!)
2. Value has extra spaces or quotes
3. Secret set in wrong repository

**Solution**: 
- Delete and recreate the secret
- Copy-paste names from documentation
- Ensure no trailing spaces in values
</details>

<details>
<summary>❌ Rate limit errors</summary>

**Error message**: `HTTP 429 Too Many Requests`

**Solutions:**
1. Increase `request_interval` in `config/config.yaml`
2. Reduce schedule frequency (e.g., every 2 hours instead of hourly)
3. Reduce number of monitored platforms

📖 More: [TROUBLESHOOTING.md](TROUBLESHOOTING.md#rate-limiting-issues)
</details>

---

## Docker Deployment

**⏱️ Time: 15 minutes** | **Difficulty: Medium** | **Self-hosted on any server**

Perfect for NAS devices, servers, or users wanting containerized deployment.

### Prerequisites
- ✅ Completed [Docker Installation](INSTALLATION.md#installation-method-3-docker-installation)
- ✅ Docker and Docker Compose installed
- ✅ Configuration files downloaded

---

### Deployment Method 1: Docker Run (Quick Test)

Simple one-command deployment for testing:

```bash
docker run -d \
  --name trend-radar \
  -v ./config:/app/config:ro \
  -v ./output:/app/output \
  -e EMAIL_FROM="your_email@example.com" \
  -e EMAIL_PASSWORD="your_app_password" \
  -e EMAIL_TO="recipient@example.com" \
  -e NTFY_TOPIC="your_topic" \
  -e CRON_SCHEDULE="*/30 * * * *" \
  -e RUN_MODE="cron" \
  -e IMMEDIATE_RUN="true" \
  wantcat/trendradar:latest
```

**Parameters explained:**
- `-d`: Run in background (detached)
- `--name trend-radar`: Container name
- `-v ./config:/app/config:ro`: Mount config folder (read-only)
- `-v ./output:/app/output`: Mount output folder (writable)
- `-e KEY="VALUE"`: Environment variables
- `wantcat/trendradar:latest`: Docker image

---

### Deployment Method 2: Docker Compose (Recommended)

Better for production use with persistent configuration.

#### 1. Prepare Configuration Files

Ensure your directory structure looks like this:

```
trendradar/
├── config/
│   ├── config.yaml
│   └── frequency_words.txt
├── docker-compose.yml
└── .env
```

#### 2. Configure Environment Variables

Edit the `.env` file with your settings:

```bash
# Core Configuration
ENABLE_CRAWLER=true
ENABLE_NOTIFICATION=true
REPORT_MODE=daily

# Push Time Window (Optional)
PUSH_WINDOW_ENABLED=false
PUSH_WINDOW_START=08:00
PUSH_WINDOW_END=22:00

# Notification Channels (Fill at least one)
EMAIL_FROM=your_email@example.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=recipient@example.com
NTFY_TOPIC=your_topic

# Schedule
CRON_SCHEDULE=*/30 * * * *
RUN_MODE=cron
IMMEDIATE_RUN=true
```

**Environment variable explanations:**

##### Core Configuration

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `ENABLE_CRAWLER` | `true`/`false` | `true` | Enable news crawling |
| `ENABLE_NOTIFICATION` | `true`/`false` | `true` | Enable push notifications |
| `REPORT_MODE` | `daily`/`incremental`/`current` | `daily` | Report push mode |

**Report modes explained:**
- **`daily`**: Push all matching news once per schedule (comprehensive)
- **`incremental`**: Push only new items (avoid duplicates)
- **`current`**: Push current rankings (real-time trending)

📖 More: [CONFIGURATION.md - Report Mode](CONFIGURATION.md#report-mode)

---

##### Push Time Window

| Variable | Format | Example | Description |
|----------|--------|---------|-------------|
| `PUSH_WINDOW_ENABLED` | `true`/`false` | `false` | Enable time window control |
| `PUSH_WINDOW_START` | `HH:MM` | `08:00` | Start time (Beijing time) |
| `PUSH_WINDOW_END` | `HH:MM` | `22:00` | End time (Beijing time) |
| `PUSH_WINDOW_ONCE_PER_DAY` | `true`/`false` | `true` | Push once per day only |
| `PUSH_WINDOW_RETENTION_DAYS` | number | `7` | Days to keep push records |

**Example use case:**
```bash
# Only receive notifications during work hours
PUSH_WINDOW_ENABLED=true
PUSH_WINDOW_START=09:00
PUSH_WINDOW_END=18:00
PUSH_WINDOW_ONCE_PER_DAY=false  # Push every execution within window
```

---

##### Cron Schedule

| Variable | Format | Example | Description |
|----------|--------|---------|-------------|
| `CRON_SCHEDULE` | Cron expression | `*/30 * * * *` | When to run crawler |
| `RUN_MODE` | `cron`/`once` | `cron` | Execution mode |
| `IMMEDIATE_RUN` | `true`/`false` | `true` | Run immediately on startup |

**Common schedules:**
```bash
# Every 30 minutes
CRON_SCHEDULE=*/30 * * * *

# Every hour
CRON_SCHEDULE=0 * * * *

# Every 2 hours
CRON_SCHEDULE=0 */2 * * *

# Every day at 9 AM
CRON_SCHEDULE=0 9 * * *

# Every 30 minutes, business hours only (9 AM - 6 PM)
CRON_SCHEDULE=*/30 9-18 * * *
```

---

#### 3. Review docker-compose.yml

The compose file should look like this:

```yaml
version: '3.8'

services:
  trendradar:
    image: wantcat/trendradar:latest
    container_name: trend-radar
    restart: unless-stopped
    
    volumes:
      - ./config:/app/config:ro     # Config files (read-only)
      - ./output:/app/output         # Output data (writable)
    
    env_file:
      - .env                         # Load environment variables
    
    environment:
      - TZ=Asia/Shanghai             # Timezone (Beijing time)
```

**💡 Configuration Priority**: Environment variables (`.env`) override `config/config.yaml` settings.

This is useful for NAS users where editing YAML files is difficult!

---

#### 4. Start Services

Pull the latest image and start:

```bash
# Navigate to project directory
cd trendradar

# Pull latest image
docker-compose pull

# Start in background
docker-compose up -d
```

**Expected output:**
```
Pulling trendradar (wantcat/trendradar:latest)...
latest: Pulling from wantcat/trendradar
...
Creating trend-radar ... done
```

✅ **Verify**: Container is running:
```bash
docker ps | grep trend-radar
```

---

### Container Management

#### View Logs

**Real-time logs (follow mode):**
```bash
docker logs -f trend-radar
```

**Last 100 lines:**
```bash
docker logs --tail 100 trend-radar
```

**Since specific time:**
```bash
docker logs --since 30m trend-radar  # Last 30 minutes
```

#### Check Status

```bash
# Container status
docker ps -a | grep trend-radar

# Detailed inspect
docker inspect trend-radar

# Resource usage
docker stats trend-radar
```

#### Restart Container

```bash
# Graceful restart
docker restart trend-radar

# Or via docker-compose
docker-compose restart
```

#### Stop Container

```bash
# Stop gracefully
docker stop trend-radar

# Or via docker-compose
docker-compose stop
```

#### Remove Container

```bash
# Stop and remove container (data in volumes is preserved)
docker-compose down

# Remove container and volumes (DELETES ALL DATA!)
docker-compose down -v
```

---

### Update Docker Image

When a new version is released:

```bash
# Pull latest image
docker pull wantcat/trendradar:latest

# Stop and remove old container
docker-compose down

# Start with new image
docker-compose up -d

# Verify new version
docker logs trend-radar | head -n 20
```

---

### Volume Management

#### Data Persistence

Docker volumes ensure data survives container restarts:

```
Host (Your Computer)     →     Container (Docker)
./config/                →     /app/config/     (read-only)
./output/                →     /app/output/     (writable)
```

#### Backup Data

```bash
# Backup output folder
tar -czf trendradar-backup-$(date +%Y%m%d).tar.gz output/

# Backup config
tar -czf trendradar-config-$(date +%Y%m%d).tar.gz config/
```

#### Clear Old Data

```bash
# Remove output files older than 30 days
find output/ -type f -mtime +30 -delete

# Keep only last 7 days
find output/ -type d -mtime +7 -exec rm -rf {} +
```

---

### Troubleshooting Docker Deployment

<details>
<summary>❌ Container exits immediately</summary>

**Check logs:**
```bash
docker logs trend-radar
```

**Common causes:**
1. Config file missing or invalid → Verify `config/config.yaml` exists
2. Environment variable error → Check `.env` file syntax
3. Permission issues → Ensure user can write to `./output/`

**Solution:**
```bash
# Test with manual run
docker run --rm \
  -v ./config:/app/config:ro \
  wantcat/trendradar:latest \
  python main.py
```
</details>

<details>
<summary>❌ Config changes not taking effect</summary>

**Problem**: NAS users editing `config.yaml` but changes don't apply.

**Solution**: Use environment variables in `.env` instead!

Environment variables override config.yaml:
```bash
# In .env file
REPORT_MODE=incremental
ENABLE_NOTIFICATION=true
```

After editing `.env`:
```bash
docker-compose restart
```
</details>

<details>
<summary>❌ Permission denied on output folder</summary>

**Error**: `PermissionError: [Errno 13] Permission denied: '/app/output/'`

**Solution**:
```bash
# Fix permissions on host
chmod -R 777 output/

# Or run container with specific user
docker-compose down
# Edit docker-compose.yml, add:
#   user: "1000:1000"
docker-compose up -d
```
</details>

<details>
<summary>❌ Cron schedule not working</summary>

**Check container logs:**
```bash
docker logs trend-radar | grep -i cron
```

**Verify cron is running:**
```bash
docker exec trend-radar ps aux | grep cron
```

**Test manual execution:**
```bash
docker exec trend-radar python main.py
```

**Common issues:**
- Invalid cron syntax → Test at [crontab.guru](https://crontab.guru/)
- `RUN_MODE` not set to `cron`
- Container timezone wrong → Set `TZ=Asia/Shanghai`
</details>

---

## Local Deployment

**⏱️ Time: 20 minutes** | **Difficulty: Advanced** | **Maximum control and flexibility**

Run TrendRadar directly on your computer with custom scheduling.

### Prerequisites
- ✅ Completed [Local Installation](INSTALLATION.md#installation-method-2-local-installation)
- ✅ Python 3.10+ installed
- ✅ Dependencies installed

---

### Method 1: Manual Execution

#### Run Once

```bash
# Activate virtual environment (if using)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Execute
python main.py
```

**Expected output:**
```
🚀 TrendRadar v3.0.5 Starting...
✅ Configuration loaded successfully
🔍 Crawling 35+ platforms...
📊 Processing 150 news items...
✅ Execution completed in 45s
```

#### Run with Custom Config

```bash
# Use different config file
python main.py --config /path/to/custom-config.yaml

# Test mode (no notifications)
python main.py --test
```

---

### Method 2: Scheduled Execution (Windows)

Use Windows Task Scheduler for automatic execution.

#### Step 1: Create Batch Script

Create `run-trendradar.bat` in your TrendRadar folder:

```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python main.py
if errorlevel 1 (
    echo Error occurred! >> error.log
    exit /b 1
)
```

**Test the script:**
```bash
run-trendradar.bat
```

---

#### Step 2: Open Task Scheduler

1. Press **Win + R**, type `taskschd.msc`, press Enter
2. Click **"Create Basic Task"** in right panel
3. Name: `TrendRadar Hourly`
4. Description: `Automated news aggregation`

---

#### Step 3: Configure Trigger

**Trigger options:**

**Option A: Hourly**
1. Select **"Daily"**, click Next
2. Set start time (e.g., 00:00)
3. Click Next
4. Select **"Repeat task every"** → **1 hour**
5. Duration: **1 day**

**Option B: Custom Times**
1. Click **"Create Task"** (advanced)
2. Triggers tab → **"New"**
3. Add multiple triggers for specific times

**Example: Business hours only (9 AM - 6 PM, every hour)**
- Create triggers for: 09:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 16:00, 17:00, 18:00

---

#### Step 4: Configure Action

1. Action: **"Start a program"**
2. Program/script: Browse to `run-trendradar.bat`
3. Start in: Your TrendRadar folder path (e.g., `C:\Users\YourName\TrendRadar`)

---

#### Step 5: Additional Settings

1. **Conditions tab:**
   - ❌ Uncheck "Start only if computer is on AC power"
   - ✅ Check "Wake the computer to run this task" (optional)

2. **Settings tab:**
   - ✅ "Allow task to be run on demand"
   - ✅ "Run task as soon as possible after a scheduled start is missed"
   - ❌ "Stop the task if it runs longer than" → Set to 1 hour

3. Click **OK** to save

---

#### Step 6: Test Scheduled Task

1. Find "TrendRadar Hourly" in Task Scheduler Library
2. Right-click → **"Run"**
3. Check "Last Run Result" → Should show "The operation completed successfully (0x0)"
4. Verify notification received

---

### Method 3: Scheduled Execution (macOS/Linux)

Use cron for automatic execution.

#### Step 1: Create Shell Script

Create `run-trendradar.sh`:

```bash
#!/bin/bash

# Navigate to TrendRadar directory
cd /path/to/TrendRadar

# Activate virtual environment
source venv/bin/activate

# Run TrendRadar
python main.py

# Log execution
echo "$(date): TrendRadar executed" >> execution.log
```

**Make executable:**
```bash
chmod +x run-trendradar.sh
```

**Test:**
```bash
./run-trendradar.sh
```

---

#### Step 2: Edit Crontab

```bash
crontab -e
```

**Add cron entries:**

```bash
# Run every hour at minute 0
0 * * * * /path/to/TrendRadar/run-trendradar.sh

# Run every 30 minutes
*/30 * * * * /path/to/TrendRadar/run-trendradar.sh

# Run every 2 hours
0 */2 * * * /path/to/TrendRadar/run-trendradar.sh

# Run twice daily (9 AM and 9 PM)
0 9,21 * * * /path/to/TrendRadar/run-trendradar.sh

# Run every weekday at 9 AM
0 9 * * 1-5 /path/to/TrendRadar/run-trendradar.sh

# Business hours (9 AM - 6 PM), every hour
0 9-18 * * * /path/to/TrendRadar/run-trendradar.sh
```

**Save and exit** (Ctrl+X, then Y, then Enter in nano)

---

#### Step 3: Verify Cron Setup

```bash
# List cron jobs
crontab -l

# Check cron logs
grep CRON /var/log/syslog  # Debian/Ubuntu
grep CRON /var/log/cron     # RedHat/CentOS

# Check execution log
tail -f /path/to/TrendRadar/execution.log
```

---

#### Step 4: Troubleshoot Cron

<details>
<summary>❌ Cron job not running</summary>

**Check cron service:**
```bash
# Check status
sudo systemctl status cron

# Start if stopped
sudo systemctl start cron
```

**Debug cron:**
```bash
# Add email notification to crontab
MAILTO=your@email.com
0 * * * * /path/to/TrendRadar/run-trendradar.sh
```

**Test with full paths:**
```bash
# Use absolute paths in crontab
0 * * * * /usr/bin/python3 /path/to/TrendRadar/main.py
```
</details>

---

### Method 4: Background Service (Linux systemd)

For always-running service with auto-restart.

#### Create Service File

Create `/etc/systemd/system/trendradar.service`:

```ini
[Unit]
Description=TrendRadar News Aggregator
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/TrendRadar
ExecStart=/path/to/TrendRadar/venv/bin/python main.py
Restart=always
RestartSec=3600

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable trendradar

# Start service
sudo systemctl start trendradar

# Check status
sudo systemctl status trendradar

# View logs
sudo journalctl -u trendradar -f
```

---

### Troubleshooting Local Deployment

<details>
<summary>❌ Script can't find Python</summary>

**Use absolute paths:**

Windows `run-trendradar.bat`:
```batch
@echo off
cd /d C:\Users\YourName\TrendRadar
C:\Users\YourName\TrendRadar\venv\Scripts\python.exe main.py
```

macOS/Linux `run-trendradar.sh`:
```bash
#!/bin/bash
cd /home/youruser/TrendRadar
/home/youruser/TrendRadar/venv/bin/python main.py
```
</details>

<details>
<summary>❌ Task Scheduler not running while locked</summary>

1. Open Task Scheduler
2. Right-click your task → Properties
3. General tab:
   - Select **"Run whether user is logged on or not"**
   - Check **"Do not store password"**
4. Click OK
</details>

<details>
<summary>❌ Cron PATH issues</summary>

**Add PATH to crontab:**
```bash
PATH=/usr/local/bin:/usr/bin:/bin
0 * * * * /path/to/TrendRadar/run-trendradar.sh
```

**Or use full paths in script:**
```bash
#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin
cd /path/to/TrendRadar
./venv/bin/python main.py
```
</details>

---

## Comparison of Deployment Methods

### Feature Comparison

| Feature | GitHub Actions | Docker | Local |
|---------|----------------|--------|-------|
| **Setup Complexity** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Advanced |
| **Maintenance** | None | Low | Medium |
| **Cost** | Free | Free | Free |
| **Execution Speed** | Variable (queue) | Fast | Fast |
| **Schedule Precision** | ±10 min | Precise | Precise |
| **Custom Code** | Via commit | Full control | Full control |
| **Offline Use** | ❌ No | ✅ Yes | ✅ Yes |
| **NAS Compatible** | N/A | ✅ Yes | ❌ No |
| **Resource Usage** | GitHub's servers | Your server | Your computer |
| **Update Method** | Git pull | Docker pull | Git pull |

### When to Use Each Method

**Choose GitHub Actions if you:**
- ✅ Want zero maintenance
- ✅ Don't have a server
- ✅ Can tolerate 10-minute schedule variance
- ✅ Need free hosting
- ✅ Want automatic updates

**Choose Docker if you:**
- ✅ Have a NAS or server
- ✅ Want containerization
- ✅ Need precise scheduling
- ✅ Want easy updates
- ✅ Prefer environment variables over config files

**Choose Local if you:**
- ✅ Want maximum control
- ✅ Need custom development
- ✅ Have a dedicated computer
- ✅ Want fastest execution
- ✅ Prefer native Python environment

---

## Next Steps

After successful deployment:

### ⚙️ Configuration
1. **[Customize keywords](CONFIGURATION.md#keyword-configuration)** - Add your interests
2. **[Adjust report mode](CONFIGURATION.md#report-mode)** - Daily/incremental/current
3. **[Configure push windows](CONFIGURATION.md#push-time-window)** - Control notification times
4. **[Tune algorithm weights](CONFIGURATION.md#weight-configuration)** - Customize trending scores

### 📊 Monitoring
1. **Check logs regularly** - Ensure smooth operation
2. **Monitor notification delivery** - Verify all channels working
3. **Review output quality** - Adjust keywords as needed
4. **Track execution times** - Optimize schedule if needed

### 🚀 Advanced Features
1. **[Enable AI analysis](../README-Cherry-Studio.md)** - Natural language queries
2. **[Set up multiple channels](CONFIGURATION.md#notification-channels-setup)** - Redundancy
3. **[Create custom platforms](CONFIGURATION.md#platforms-configuration)** - Add sources
4. **[Implement backup strategy](#volume-management)** - Protect your data

---

## Getting Help

### 📚 Documentation
- **[Configuration Guide](CONFIGURATION.md)** - Detailed settings reference
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- **[API Reference](API_REFERENCE.md)** - Technical details

### 💬 Community Support
- **[GitHub Issues](https://github.com/sansan0/TrendRadar/issues)** - Report problems
- **[Discussions](https://github.com/sansan0/TrendRadar/discussions)** - Ask questions

---

[← Back to Installation](INSTALLATION.md) | [Next: Configuration Guide →](CONFIGURATION.md)
