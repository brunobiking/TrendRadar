# Installation Guide

**⏱️ Time Estimate: 10-30 minutes (depending on method)**

Complete installation guide for TrendRadar covering all deployment methods.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Method 1: GitHub Fork (Recommended)](#installation-method-1-github-fork-recommended)
- [Installation Method 2: Local Installation](#installation-method-2-local-installation)
- [Installation Method 3: Docker Installation](#installation-method-3-docker-installation)
- [Verify Installation](#verify-installation)
- [Next Steps](#next-steps)

---

## Prerequisites

### Required Accounts
- ✅ **GitHub Account** (free) - [Sign up here](https://github.com/join)
  - Required for: GitHub Actions deployment, accessing repository
  - Benefits: Free hosting, automated scheduling, no server needed

### System Requirements

Choose requirements based on your installation method:

#### For GitHub Fork Method (Recommended)
- ✅ Web browser (Chrome, Firefox, Safari, Edge)
- ✅ Internet connection
- ❌ No local software required!

#### For Local Installation
- ✅ **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- ✅ **Git** - [Download Git](https://git-scm.com/downloads)
- ✅ 100 MB free disk space
- ✅ Internet connection

#### For Docker Installation
- ✅ **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
- ✅ **Docker Compose** (included with Docker Desktop)
- ✅ 500 MB free disk space
- ✅ Internet connection

### Operating System Compatibility

| OS | GitHub Fork | Local Install | Docker |
|----|-------------|---------------|--------|
| **Windows** 10/11 | ✅ | ✅ | ✅ |
| **macOS** 10.15+ | ✅ | ✅ | ✅ |
| **Linux** (Ubuntu/Debian) | ✅ | ✅ | ✅ |
| **NAS** (Synology/QNAP) | ✅ | ❌ | ✅ |

---

## Installation Method 1: GitHub Fork (Recommended)

**⏱️ Time: 5 minutes** | **Difficulty: Beginner** | **Cost: Free**

Best for users who want zero-maintenance automated deployment.

### Why Choose This Method?
✅ No software installation required  
✅ Runs automatically on GitHub's servers (free)  
✅ Easy to update and maintain  
✅ Built-in scheduling and logging  
✅ Perfect for beginners  

### Step-by-Step Instructions

#### 1. Fork the Repository

1. **Visit the TrendRadar repository**: https://github.com/sansan0/TrendRadar
2. **Click the "Fork" button** at the top right of the page
   - GitHub will ask "Where should we fork TrendRadar?"
   - Select your personal account
3. **Wait for the fork to complete** (usually takes 5-10 seconds)

✅ **Verify Success**: You should now see the repository at:
```
https://github.com/YOUR-USERNAME/TrendRadar
```

**Screenshot reference location**: (Fork button location)
![Fork Button](images/fork-button.png)

---

#### 2. Verify Fork Contents

After forking, check that these files exist in your repository:

Required files:
- ✅ `config/config.yaml` - Main configuration file
- ✅ `config/frequency_words.txt` - Keyword configuration
- ✅ `.github/workflows/crawler.yml` - Automation workflow
- ✅ `main.py` - Main program
- ✅ `requirements.txt` - Python dependencies

To verify:
1. Browse your forked repository
2. Click on each folder to confirm files are present
3. If any file is missing, the fork may have failed - try forking again

---

#### 3. Enable GitHub Actions

GitHub Actions must be manually enabled in forked repositories.

1. In your forked repository, click the **"Actions"** tab
2. You should see a message: "Workflows aren't being run on this forked repository"
3. Click the green button: **"I understand my workflows, go ahead and enable them"**

✅ **Verify Success**: 
- The Actions tab shows workflow list
- You can see "Hot News Crawler" workflow

**Screenshot reference location**: (Actions tab and enable button)
![Enable Actions](images/enable-actions.png)

---

#### 4. Configure Repository Settings (Optional but Recommended)

For better security and functionality:

1. Go to **Settings** → **General**
2. Under "Features", enable:
   - ✅ Issues (for bug reports)
   - ✅ Discussions (optional, for community support)
3. Under "Pull Requests", disable:
   - ❌ Allow merge commits (not needed for personal use)

---

### ✅ Fork Installation Complete!

Your TrendRadar is now installed on GitHub. 

**What happens next:**
- The crawler will run automatically every hour (configurable)
- Notifications will be sent to your configured channels
- All news data is saved in the `output/` folder

**Next:** Proceed to [Configuration Guide](CONFIGURATION.md) to set up your notification channels and keywords.

---

## Installation Method 2: Local Installation

**⏱️ Time: 15 minutes** | **Difficulty: Intermediate** | **Cost: Free**

Best for users who want full control, offline access, or custom development.

### Why Choose This Method?
✅ Run on your own computer  
✅ Faster execution (no GitHub Actions queue)  
✅ More flexible scheduling  
✅ Full control over data and configuration  
✅ Can customize code  

### Prerequisites Check

Before starting, verify you have:

#### Check Python Version

**Windows:**
```bash
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

Expected output: `Python 3.10.0` or higher

❌ **If Python is not installed or version is too old:**
- Download from: https://www.python.org/downloads/
- During installation on Windows, check **"Add Python to PATH"**

---

#### Check Git Installation

```bash
git --version
```

Expected output: `git version 2.x.x`

❌ **If Git is not installed:**
- Windows: Download from https://git-scm.com/download/win
- macOS: Install Xcode Command Line Tools: `xcode-select --install`
- Linux: `sudo apt-get install git` (Debian/Ubuntu) or `sudo yum install git` (RedHat/CentOS)

---

### Step-by-Step Instructions

#### 1. Clone the Repository

**Option A: Clone Original Repository**
```bash
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar
```

**Option B: Clone Your Fork (if you forked it)**
```bash
git clone https://github.com/YOUR-USERNAME/TrendRadar.git
cd TrendRadar
```

✅ **Verify Success**: You should see a `TrendRadar` folder with all project files.

---

#### 2. Set Up Python Environment (Recommended)

Using a virtual environment keeps TrendRadar's dependencies isolated.

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

✅ **Verify Success**: Your command prompt should show `(venv)` prefix.

**💡 Tip**: To deactivate later, just type: `deactivate`

---

#### 3. Install Dependencies

TrendRadar requires these Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| requests | ≥2.32.5, <3.0.0 | HTTP requests to news APIs |
| pytz | ≥2025.2, <2026.0 | Timezone handling (Beijing time) |
| PyYAML | ≥6.0.3, <7.0.0 | YAML configuration parsing |
| fastmcp | ≥2.12.0, <2.14.0 | MCP server for AI analysis |
| websockets | ≥13.0, <14.0 | WebSocket support for MCP |

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Installation progress:**
```
Collecting requests>=2.32.5
  Downloading requests-2.32.5-py3-none-any.whl
Collecting pytz>=2025.2
  Downloading pytz-2025.2-py2.py3-none-any.whl
...
Successfully installed requests-2.32.5 pytz-2025.2 PyYAML-6.0.3 ...
```

✅ **Verify Success**: No error messages during installation.

**Common Issues:**

<details>
<summary>❌ "pip: command not found"</summary>

Try using `pip3` instead:
```bash
pip3 install -r requirements.txt
```
</details>

<details>
<summary>❌ "Permission denied"</summary>

On Linux/macOS, try with sudo (only if not using virtual environment):
```bash
sudo pip3 install -r requirements.txt
```

Better solution: Use virtual environment as described in Step 2.
</details>

---

#### 4. Run Setup Script (Optional)

TrendRadar provides setup scripts for easier configuration:

**Windows:**
```bash
setup-windows-en.bat
```

**macOS/Linux:**
```bash
chmod +x setup-mac.sh
./setup-mac.sh
```

These scripts will:
- Verify Python installation
- Install dependencies
- Check configuration files
- Test the installation

---

#### 5. Test Local Installation

Run TrendRadar manually to verify installation:

```bash
python main.py
```

**Expected output:**
```
🚀 TrendRadar v3.0.5 Starting...
✅ Configuration loaded successfully
🔍 Crawling news from 35+ platforms...
📊 Processing trending topics...
✅ Execution completed successfully
```

✅ **Verify Success**: 
- No error messages
- `output/` folder created with HTML/TXT files
- If notifications configured, you receive a test message

**Common Issues:**

<details>
<summary>❌ "ModuleNotFoundError: No module named 'requests'"</summary>

Dependencies not installed. Run:
```bash
pip install -r requirements.txt
```
</details>

<details>
<summary>❌ "FileNotFoundError: config/config.yaml"</summary>

Configuration file missing. Ensure you're in the TrendRadar directory:
```bash
cd TrendRadar
ls config/
```

You should see `config.yaml` and `frequency_words.txt`.
</details>

---

### ✅ Local Installation Complete!

Your TrendRadar is now installed locally.

**Next steps:**
1. Configure notification channels: [CONFIGURATION.md](CONFIGURATION.md)
2. Set up scheduled execution: [DEPLOYMENT.md](DEPLOYMENT.md#local-deployment)
3. Customize keywords: [CONFIGURATION.md](CONFIGURATION.md#keyword-configuration)

---

## Installation Method 3: Docker Installation

**⏱️ Time: 10 minutes** | **Difficulty: Intermediate** | **Cost: Free**

Best for users who want containerized deployment, easy updates, or NAS deployment.

### Why Choose This Method?
✅ Consistent environment across all systems  
✅ Easy to update (pull new image)  
✅ Isolated from host system  
✅ Perfect for NAS devices (Synology, QNAP)  
✅ No Python installation needed  

### Prerequisites Check

#### Check Docker Installation

```bash
docker --version
docker-compose --version
```

Expected output:
```
Docker version 20.10.x or higher
Docker Compose version 2.x.x or higher
```

❌ **If Docker is not installed:**

**Windows/macOS:**
- Download Docker Desktop: https://www.docker.com/products/docker-desktop

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

**Synology NAS:**
1. Open Package Center
2. Search for "Docker"
3. Click Install

---

### Step-by-Step Instructions

#### 1. Create Project Directory

```bash
# Create directory structure
mkdir -p trendradar/config
cd trendradar
```

---

#### 2. Download Configuration Files

**Option A: Using wget (Linux/macOS/Git Bash on Windows):**
```bash
# Download config files
wget https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/config.yaml -P config/
wget https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/frequency_words.txt -P config/
```

**Option B: Using curl (if wget not available):**
```bash
curl -o config/config.yaml https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/config.yaml
curl -o config/frequency_words.txt https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/frequency_words.txt
```

**Option C: Manual Download (Windows/any browser):**
1. Visit: https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/config.yaml
2. Right-click → "Save As" → Save to `trendradar/config/config.yaml`
3. Visit: https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/frequency_words.txt
4. Right-click → "Save As" → Save to `trendradar/config/frequency_words.txt`

---

#### 3. Download Docker Configuration

**Download docker-compose.yml and .env:**
```bash
# Download Docker configuration
wget https://raw.githubusercontent.com/sansan0/TrendRadar/master/docker/docker-compose.yml
wget https://raw.githubusercontent.com/sansan0/TrendRadar/master/docker/.env
```

**Or manually download:**
1. Create `docker-compose.yml` from: https://github.com/sansan0/TrendRadar/blob/master/docker/docker-compose.yml
2. Create `.env` from: https://github.com/sansan0/TrendRadar/blob/master/docker/.env

---

#### 4. Verify Directory Structure

Your directory should look like this:

```
trendradar/
├── config/
│   ├── config.yaml
│   └── frequency_words.txt
├── docker-compose.yml
└── .env
```

Verify with:
```bash
ls -la
ls -la config/
```

---

#### 5. Pull Docker Image

TrendRadar provides pre-built multi-architecture images:

```bash
docker pull wantcat/trendradar:latest
```

**Expected output:**
```
latest: Pulling from wantcat/trendradar
a1b2c3d4e5f6: Pull complete
...
Status: Downloaded newer image for wantcat/trendradar:latest
```

**Image details:**
- **Image name**: `wantcat/trendradar`
- **Architectures supported**: 
  - linux/amd64 (Intel/AMD 64-bit)
  - linux/arm64 (ARM 64-bit, Apple Silicon, Raspberry Pi)
  - linux/arm/v7 (ARM 32-bit)

---

#### 6. Test Docker Installation

Run a quick test without persistent configuration:

```bash
docker run --rm wantcat/trendradar:latest python --version
```

Expected output: `Python 3.10.x` or higher

✅ **Verify Success**: No error messages.

---

### ✅ Docker Installation Complete!

Your TrendRadar Docker image is now installed and ready to deploy.

**Next steps:**
1. Configure environment variables: [DEPLOYMENT.md](DEPLOYMENT.md#docker-deployment)
2. Configure notification channels: [CONFIGURATION.md](CONFIGURATION.md)
3. Start the container: [DEPLOYMENT.md](DEPLOYMENT.md#docker-deployment)

---

## Verify Installation

After completing any installation method, verify everything is working:

### 1. Check Configuration Files

**For GitHub Fork / Local:**
```bash
# Verify config files exist
ls -la config/config.yaml
ls -la config/frequency_words.txt
```

**For Docker:**
```bash
# Verify mounted config
docker run --rm -v ./config:/app/config wantcat/trendradar:latest ls -la /app/config
```

---

### 2. Run Test Execution

**GitHub Fork:**
- Go to Actions tab → Hot News Crawler → Run workflow

**Local:**
```bash
python main.py
```

**Docker:**
```bash
docker run --rm \
  -v ./config:/app/config:ro \
  -v ./output:/app/output \
  wantcat/trendradar:latest \
  python main.py
```

---

### 3. Check Output

After execution, verify:

✅ **Output folder created**: Contains HTML and TXT files with news data  
✅ **No error messages**: Check console output or logs  
✅ **Notification received**: If configured, test message on your device  

**Output folder structure:**
```
output/
└── 2025年01月15日/
    ├── html/
    │   └── 12时30分.html
    └── txt/
        └── 12时30分.txt
```

---

## Troubleshooting Installation Issues

### Common Issues

<details>
<summary>❌ GitHub Fork: Actions not running</summary>

**Problem**: Forked workflow doesn't execute automatically.

**Solutions**:
1. Check Actions are enabled: Actions tab → "Enable workflows"
2. Verify cron schedule is valid in `.github/workflows/crawler.yml`
3. Check GitHub Actions status: https://www.githubstatus.com/
4. Manual trigger: Actions → Hot News Crawler → Run workflow

📖 More: [TROUBLESHOOTING.md](TROUBLESHOOTING.md#github-actions-not-running)
</details>

<details>
<summary>❌ Local: Python version too old</summary>

**Problem**: `SyntaxError` or "requires Python 3.10+"

**Solution**:
1. Update Python: https://www.python.org/downloads/
2. Use pyenv to manage multiple Python versions:
   ```bash
   # Install pyenv, then:
   pyenv install 3.10
   pyenv local 3.10
   ```
</details>

<details>
<summary>❌ Docker: Container won't start</summary>

**Problem**: Container exits immediately or fails to start.

**Solutions**:
1. Check Docker logs:
   ```bash
   docker logs trend-radar
   ```
2. Verify config files exist and are mounted correctly
3. Check environment variables in `.env`
4. Ensure ports aren't already in use

📖 More: [TROUBLESHOOTING.md](TROUBLESHOOTING.md#docker-container-issues)
</details>

<details>
<summary>❌ Dependency installation fails</summary>

**Problem**: `pip install` errors or package conflicts.

**Solutions**:
1. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```
2. Use virtual environment (recommended)
3. Install packages one by one to identify the problematic one
4. Check Python version compatibility
</details>

---

## Next Steps

Now that installation is complete, proceed with configuration:

### 🔧 Essential Configuration (Required)
1. **[Set up notification channels](CONFIGURATION.md#notification-channels-setup)**
   - Configure at least one notification method
   - Test notifications

2. **[Configure keywords](CONFIGURATION.md#keyword-configuration)**
   - Customize `frequency_words.txt`
   - Add topics you care about

### ⚙️ Advanced Configuration (Optional)
3. **[Choose report mode](CONFIGURATION.md#report-mode)**
   - Daily, current, or incremental

4. **[Set up push time windows](CONFIGURATION.md#push-time-window)**
   - Control when notifications are sent

5. **[Customize trending algorithm](CONFIGURATION.md#weight-configuration)**
   - Adjust ranking weights

### 🚀 Deployment
6. **[Deploy your chosen method](DEPLOYMENT.md)**
   - GitHub Actions scheduling
   - Docker container management
   - Local scheduled execution

---

## Getting Help

### 📚 Documentation
- **[Quick Start Guide](QUICKSTART.md)** - 5-minute setup
- **[Configuration Guide](CONFIGURATION.md)** - Detailed settings
- **[Deployment Guide](DEPLOYMENT.md)** - Running methods
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common problems

### 💬 Community Support
- **GitHub Issues**: [Report installation problems](https://github.com/sansan0/TrendRadar/issues)
- **Discussions**: [Ask installation questions](https://github.com/sansan0/TrendRadar/discussions)

---

[← Back to Quick Start](QUICKSTART.md) | [Next: Configuration Guide →](CONFIGURATION.md)
