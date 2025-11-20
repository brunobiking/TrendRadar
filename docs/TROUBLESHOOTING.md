# Troubleshooting Guide

**⏱️ Time Estimate: 5-30 minutes to resolve most issues**

Comprehensive solutions to common TrendRadar problems.

## Table of Contents
- [Quick Diagnosis](#quick-diagnosis)
- [Common Issues](#common-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Debug Steps](#debug-steps)
- [Error Messages Reference](#error-messages-reference)
- [Getting Additional Help](#getting-additional-help)

---

## Quick Diagnosis

Start here to quickly identify your problem:

### ❓ Symptoms Checklist

| Symptom | Likely Cause | Section |
|---------|--------------|---------|
| No notifications received | Configuration issue | [No Notifications](#1-no-notifications-received) |
| GitHub Actions not running | Workflow not enabled | [GitHub Actions Issues](#2-github-actions-not-running) |
| Docker container won't start | Config or permission error | [Docker Issues](#3-docker-container-issues) |
| Empty notifications | Keyword config too strict | [Empty Data](#4-empty-or-no-data) |
| Email not sending | SMTP authentication | [Email Issues](#5-email-sending-failures) |
| Rate limit errors | Too many requests | [Rate Limiting](#6-rate-limiting-issues) |

**💡 Pro Tip:** Check [logs](#view-logs) first - they usually reveal the problem!

---

## Common Issues

### 1. No Notifications Received

**Symptom:** TrendRadar runs successfully but no notifications arrive on your device.

#### Check 1: Notification Enabled?

**Verify in `config/config.yaml`:**
```yaml
notification:
  enable_notification: true  # Must be true!
```

**Or check environment variable (Docker):**
```bash
docker exec trend-radar env | grep ENABLE_NOTIFICATION
# Should show: ENABLE_NOTIFICATION=true
```

**Fix:**
```yaml
notification:
  enable_notification: true
```

---

#### Check 2: Webhook/Token Configured?

**Verify GitHub Secrets exist:**
1. Go to repository → Settings → Secrets → Actions
2. Confirm at least one notification secret is set:
   - `EMAIL_FROM` + `EMAIL_PASSWORD` + `EMAIL_TO`
   - `NTFY_TOPIC`

**Common mistakes:**
- ❌ Secret name typo (case-sensitive!)
- ❌ Value has extra spaces or quotes
- ❌ Secret set in wrong repository

**Fix:** Delete and recreate secrets with exact names from [CONFIGURATION.md](CONFIGURATION.md#notification-channels-setup).

---

#### Check 3: Push Time Window Blocking?

**Verify push window settings:**
```yaml
notification:
  push_window:
    enabled: false  # If true, check time range
    time_range:
      start: "08:00"
      end: "22:00"
```

**If enabled:**
- Check current Beijing time: https://time.is/Beijing
- Ensure execution time falls within window
- Check `once_per_day` - may have already pushed today

**Debug - Temporarily disable:**
```yaml
push_window:
  enabled: false
```

---

#### Check 4: Keyword Matching

**Verify keywords are matching news:**

1. Check `frequency_words.txt` isn't too restrictive
2. Temporarily use very broad keywords:
   ```txt
   news
   today
   trending
   ```
3. Run test execution
4. If notifications now work → Original keywords too strict

**See:** [Keyword Configuration](CONFIGURATION.md#keyword-configuration) for tuning tips.

---

#### Check 5: Test Webhook Directly

**ntfy:**
```bash
curl -d "Manual test" ntfy.sh/<YOUR_TOPIC>
```

**Email:**
Test email sending using Python:
```bash
python3 -c "
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Manual test from TrendRadar')
msg['Subject'] = 'Test Message'
msg['From'] = 'your_email@example.com'
msg['To'] = 'recipient@example.com'

with smtplib.SMTP('smtp.example.com', 587) as server:
    server.starttls()
    server.login('your_email@example.com', 'your_password')
    server.send_message(msg)
print('Email sent successfully!')
"
```

**Expected:** Message appears on your device or in your inbox.

**If test fails:** Problem is with webhook/email configuration, not TrendRadar.

---

### 2. GitHub Actions Not Running

**Symptom:** Forked workflow doesn't execute on schedule or manually.

#### Check 1: Actions Enabled?

1. Go to **Actions** tab in your repository
2. Look for message: "Workflows aren't being run on this forked repository"
3. Click **"I understand my workflows, go ahead and enable them"**

**Fix:** Enable workflows, then manually trigger once.

---

#### Check 2: Workflow File Valid?

**Check `.github/workflows/crawler.yml` exists and has correct syntax:**

```bash
# Clone your repo locally
git clone https://github.com/YOUR_USERNAME/TrendRadar.git
cd TrendRadar

# Verify file exists
ls -la .github/workflows/crawler.yml

# Check syntax (online)
```

Visit: https://crontab.guru/ to validate your cron expression.

**Common issues:**
- File accidentally deleted
- Invalid YAML syntax
- Incorrect cron expression

**Fix:** Compare with [original file](https://github.com/sansan0/TrendRadar/blob/master/.github/workflows/crawler.yml).

---

#### Check 3: Workflow Runs History

1. Actions tab → Hot News Crawler
2. Check run history

**Scenarios:**

**No runs at all:**
- Actions not enabled → See Check 1
- Schedule not reached yet → Wait for first cron time

**Runs failing:**
- Click failed run → View logs → See error
- Go to [Error Messages Reference](#error-messages-reference)

**Runs canceled:**
- Check repository settings → Actions → Allow all actions

---

#### Check 4: GitHub Actions Status

Sometimes GitHub has outages:

1. Visit: https://www.githubstatus.com/
2. Check "Actions" service status
3. If degraded → Wait and retry later

---

#### Check 5: Re-Fork Repository

Last resort if all else fails:

1. Delete your fork (Settings → scroll to bottom → Delete repository)
2. Fork again from original: https://github.com/sansan0/TrendRadar
3. Re-configure secrets
4. Enable Actions

---

### 3. Docker Container Issues

**Symptom:** Container won't start or exits immediately.

#### Check 1: View Container Logs

```bash
docker logs trend-radar
```

Common errors and fixes below.

---

#### Check 2: Config Files Missing

**Error in logs:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/app/config/config.yaml'
```

**Cause:** Config folder not mounted or files missing.

**Fix:**
```bash
# Check your directory structure
ls -la config/

# Should see:
# config.yaml
# frequency_words.txt

# If missing, download them:
wget https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/config.yaml -P config/
wget https://raw.githubusercontent.com/sansan0/TrendRadar/master/config/frequency_words.txt -P config/
```

**Verify mount in docker-compose.yml:**
```yaml
volumes:
  - ./config:/app/config:ro  # Path relative to docker-compose.yml location
  - ./output:/app/output
```

---

#### Check 3: Permission Errors

**Error in logs:**
```
PermissionError: [Errno 13] Permission denied: '/app/output/'
```

**Cause:** Container can't write to output folder.

**Fix - Method 1 (Quick):**
```bash
chmod -R 777 output/
docker restart trend-radar
```

**Fix - Method 2 (Better):**
```bash
# Find container user ID
docker exec trend-radar id

# Change output folder ownership
sudo chown -R 1000:1000 output/  # Replace 1000 with actual UID

# Restart
docker restart trend-radar
```

**Fix - Method 3 (Docker Compose):**
Add to `docker-compose.yml`:
```yaml
services:
  trendradar:
    user: "1000:1000"  # Your user:group ID
```

Then:
```bash
docker-compose down
docker-compose up -d
```

---

#### Check 4: Port Conflicts

**Error in logs:**
```
Error: bind: address already in use
```

**Cause:** Another service using the same port (if running MCP server).

**Fix:**
```bash
# Find what's using port 3333 (if running HTTP mode)
lsof -i :3333  # macOS/Linux
netstat -ano | findstr :3333  # Windows

# Kill the process or use different port
docker run -p 3334:3333 ...  # Use host port 3334
```

---

#### Check 5: Environment Variables

**Error in logs:**
```
REPORT_MODE must be one of: daily, incremental, current
```

**Cause:** Invalid environment variable value.

**Fix - Check .env file:**
```bash
cat .env | grep REPORT_MODE
# Should be: REPORT_MODE=daily or incremental or current

# Fix syntax:
# BAD:  REPORT_MODE = "daily"  (spaces and quotes cause issues)
# GOOD: REPORT_MODE=daily
```

**Restart after fixing:**
```bash
docker-compose restart
```

---

#### Check 6: Container Resource Limits

**Symptom:** Container starts but crashes randomly.

**Check logs for:**
```
Killed
Out of memory
```

**Fix - Increase resources:**

Docker Desktop → Settings → Resources:
- RAM: At least 2GB
- CPU: At least 2 cores

Or in docker-compose.yml:
```yaml
services:
  trendradar:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

---

### 4. Empty or No Data

**Symptom:** Notifications sent but contain no news items.

#### Cause 1: Keywords Too Strict

**Check `frequency_words.txt`:**

**Problem configuration:**
```txt
Apple iPhone
+launch
+today
+official
!rumor
!leak
!speculation
```

This is TOO restrictive - requires ALL these conditions!

**Fix - Relax constraints:**
```txt
Apple
iPhone
+launch
!rumor
```

**Test with very broad keywords:**
```txt
news
trending
```

If this works → Original keywords too strict.

---

#### Cause 2: All Platforms Failing

**Check logs for:**
```
Error fetching from platform 'zhihu': Connection timeout
Error fetching from platform 'weibo': HTTP 403
```

**Possible reasons:**
- API is down (temporary)
- Rate limited (too many requests)
- Network issue (firewall, proxy)

**Fix:**
1. Wait 10-15 minutes and retry
2. Check network connectivity
3. Try with proxy if blocked:
   ```yaml
   crawler:
     use_proxy: true
     default_proxy: "http://127.0.0.1:7890"
   ```

---

#### Cause 3: Filter Words Blocking Everything

**Check for overly broad filter words:**

**Problem:**
```txt
Apple
Tesla
!news  # This blocks almost everything!
```

**Fix - Be specific with filters:**
```txt
Apple
Tesla
!advertisement
!sponsored
```

---

### 5. Email Sending Failures

**Symptom:** Email notification fails with authentication or connection errors.

#### Error 1: Authentication Failed

**Error message:**
```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
```

**Cause:** Using account password instead of app password.

**Fix:**

**Gmail:**
1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Generate App Password
4. Use app password, NOT your account password

**QQ Mail:**
1. Login web version → Settings → Account
2. Enable POP3/SMTP
3. Generate authorization code (16 chars)
4. Use authorization code, NOT QQ password

**163/126 Mail:**
1. Settings → POP3/SMTP/IMAP
2. Enable SMTP
3. Get authorization code
4. Use authorization code

**Update configuration:**
```yaml
notification:
  webhooks:
    email_password: "your-app-password-here"  # NOT account password!
```

---

#### Error 2: SMTP Connection Refused

**Error message:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Cause:** Wrong SMTP server or port.

**Fix - Manually specify SMTP settings:**

```yaml
notification:
  webhooks:
    email_smtp_server: "smtp.gmail.com"  # Gmail
    email_smtp_port: "587"  # TLS port

    # Or for SSL:
    # email_smtp_port: "465"
```

**Common SMTP settings:**

| Provider | Server | Port | Type |
|----------|--------|------|------|
| Gmail | smtp.gmail.com | 587 | TLS |
| QQ Mail | smtp.qq.com | 465 | SSL |
| Outlook | smtp-mail.outlook.com | 587 | TLS |
| 163 Mail | smtp.163.com | 465 | SSL |

---

#### Error 3: TLS/SSL Version Mismatch

**Error message:**
```
ssl.SSLError: [SSL: WRONG_VERSION_NUMBER]
```

**Cause:** Using wrong port for encryption type.

**Fix:**
- Port 587 → Use STARTTLS
- Port 465 → Use SSL

Try alternate port:
```yaml
email_smtp_port: "465"  # If 587 fails, try 465
```

---

#### Error 4: Firewall Blocking

**Error message:**
```
TimeoutError: [Errno 110] Connection timed out
```

**Cause:** Firewall or network blocking SMTP ports.

**Fix:**
1. Check firewall settings
2. Try from different network
3. Contact IT department if on corporate network
4. Use VPN or proxy

---

### 6. Rate Limiting Issues

**Symptom:** Getting HTTP 429 errors or some platforms stop returning data.

#### Error Message

```
HTTP Error 429: Too Many Requests
Rate limit exceeded for platform 'zhihu'
```

#### Cause

Making requests too fast to news APIs.

#### Fix 1: Increase Request Interval

**In `config/config.yaml`:**
```yaml
crawler:
  request_interval: 2000  # Increase from 1000 to 2000ms
```

**Try intervals:**
- Light use: 1000ms (default)
- Moderate: 2000ms
- Heavy use: 3000ms
- Still failing: 5000ms

---

#### Fix 2: Reduce Platform Count

**Comment out some platforms:**
```yaml
platforms:
  - id: "zhihu"
    name: "Zhihu"
  - id: "weibo"
    name: "Weibo"
  # - id: "toutiao"    # Disabled
  #   name: "Toutiao"  # Disabled
```

---

#### Fix 3: Reduce Execution Frequency

**GitHub Actions - Less frequent:**
```yaml
schedule:
  - cron: "0 */2 * * *"  # Every 2 hours instead of every hour
```

**Docker - Adjust cron:**
```bash
# In .env
CRON_SCHEDULE=0 */2 * * *  # Every 2 hours
```

---

#### Fix 4: Use Proxy

**If rate limited by IP:**
```yaml
crawler:
  use_proxy: true
  default_proxy: "http://127.0.0.1:7890"
```

**Or rotate proxies** (requires custom code modification).

---

### 7. Configuration File Errors

**Symptom:** YAML parsing errors when starting.

#### Error 1: Invalid YAML Syntax

**Error message:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Common causes:**

**Cause 1 - Missing quotes:**
```yaml
# BAD
webhook_url: https://example.com?key=value

# GOOD
webhook_url: "https://example.com?key=value"
```

**Cause 2 - Wrong indentation:**
```yaml
# BAD (mixing spaces and tabs)
notification:
  enable_notification: true
	message_batch_size: 4000

# GOOD (consistent spaces)
notification:
  enable_notification: true
  message_batch_size: 4000
```

**Cause 3 - Special characters:**
```yaml
# BAD
password: my:p@ssw0rd!

# GOOD
password: "my:p@ssw0rd!"
```

**Fix - Validate YAML:**
```bash
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
# No output = valid
```

Or use online validator: https://www.yamllint.com/

---

#### Error 2: Missing Required Fields

**Error message:**
```
KeyError: 'notification'
Configuration validation failed
```

**Fix - Restore missing sections:**

Compare your config.yaml with [default config](https://github.com/sansan0/TrendRadar/blob/master/config/config.yaml).

Restore any missing sections:
```yaml
app:
  version_check_url: "..."
  show_version_update: true

crawler:
  request_interval: 1000
  enable_crawler: true
  # ... etc

notification:
  enable_notification: true
  # ... etc
```

---

### 8. Keyword Matching Issues

**Symptom:** Keywords not matching expected news.

#### Issue 1: Case Sensitivity

Keywords are **case-insensitive** by default.

```txt
apple  = Apple = APPLE  (all match "Apple announces...")
```

**No action needed** - this works as expected.

---

#### Issue 2: Partial Matching

Keywords match **anywhere in title**:

```txt
# Keyword: "phone"

✅ Matches:
- "New smartphone released"
- "iPhone 15 launched"
- "Telephone company merger"

❌ Does NOT match:
- "New mobile device"
- "Cell release today"
```

**Fix - Add variations:**
```txt
phone
smartphone
mobile
iPhone
Android
```

---

#### Issue 3: Required Words Logic

**Misunderstanding:** "Required word applies to ALL keywords"

**Reality:** Required word + ANY normal keyword

**Example:**
```txt
Apple
Tesla
+phone
```

**Matches:**
- ✅ "Apple phone" (Apple + phone)
- ✅ "Tesla phone" (Tesla + phone)
- ❌ "Apple car" (Apple but no phone)
- ❌ "Tesla stock" (Tesla but no phone)

**If you want Apple OR Tesla (without requirement):**
```txt
# Group 1 - With phone requirement
Apple
Tesla
+phone

# Group 2 - Without requirement (add empty line)

Apple
Tesla
```

---

### 9. GitHub Pages Not Working

**Symptom:** GitHub Pages site shows 404 or not updating.

#### Check 1: Pages Enabled?

1. Settings → Pages
2. Verify "Source" is set to "Deploy from a branch"
3. Verify branch is "main" or "master"
4. Verify folder is "/ (root)"

---

#### Check 2: Workflow Committing Files?

**Check commit history:**
1. Repository → Commits
2. Look for: "Auto update by GitHub Actions"

**If no auto-commits:**
- Workflow may not have permissions
- Check `.github/workflows/crawler.yml` has:
  ```yaml
  permissions:
    contents: write
  ```

---

#### Check 3: index.html Exists?

```bash
# Check repository root
ls -la index.html

# Should exist with recent timestamp
```

**If missing:**
- Workflow didn't run successfully
- Output generation failed
- Check workflow logs

---

#### Check 4: GitHub Pages Build Logs

1. Actions tab
2. Look for "pages build and deployment" workflow
3. Check for errors

Common issues:
- index.html has invalid HTML
- Assets too large (>100MB)
- Too many files

---

### 10. AI Analysis / MCP Issues

**Symptom:** MCP server won't start or clients can't connect.

#### Issue 1: HTTP Server Won't Start

**Error:**
```
Address already in use: 3333
```

**Fix:**
```bash
# Find what's using port 3333
lsof -i :3333

# Kill the process or use different port
uv run python -m mcp_server.server --transport http --port 3334
```

---

#### Issue 2: Dependencies Missing

**Error:**
```
ModuleNotFoundError: No module named 'fastmcp'
```

**Fix:**
```bash
# Re-install dependencies
pip install -r requirements.txt

# Or specifically:
pip install fastmcp>=2.12.0 websockets>=13.0
```

---

#### Issue 3: No Data Available

**Error from AI:**
```
"No news data found for the specified date"
```

**Cause:** Output folder empty or no data for requested date.

**Fix:**
1. Run crawler first: `python main.py`
2. Check output folder: `ls output/`
3. Verify data exists for the date you're querying

**Remember:** AI analyzes LOCAL data in `output/`, not live web data!

---

## Platform-Specific Issues

### Email Issues

<details>
<summary>❌ Email in spam folder</summary>

**Cause:** New sender, low reputation.

**Fix:**
1. Mark as "Not Spam"
2. Add sender to contacts
3. Create filter to always inbox
</details>

<details>
<summary>❌ "Relay access denied"</summary>

**Cause:** SMTP server requires authentication or rejecting connection.

**Fix:**
1. Verify email_from matches authentication account
2. Check SMTP server allows external clients
3. Try port 465 instead of 587
</details>

---

### ntfy Issues

<details>
<summary>❌ Not receiving on device</summary>

**Check:**
1. App has notification permissions (iOS/Android settings)
2. Topic name matches exactly (case-sensitive)
3. Test in browser: https://ntfy.sh/your-topic-name

**Browser test:** If notifications appear in browser but not app → App issue
</details>

<details>
<summary>❌ "403 Forbidden" on self-hosted</summary>

**Cause:** Authentication enabled but not configured.

**Fix:**
```yaml
ntfy_token: "tk_your_token_here"
```

Get token from your ntfy server.
</details>

---

## Debug Steps

### View Logs

#### GitHub Actions

1. Actions tab
2. Click workflow run
3. Click "crawl" job
4. Expand each step to see logs

**Key sections:**
- "Run crawler" - Main execution
- Errors usually at the end

---

#### Docker

```bash
# Real-time logs
docker logs -f trend-radar

# Last 100 lines
docker logs --tail 100 trend-radar

# Since 30 minutes ago
docker logs --since 30m trend-radar

# Save logs to file
docker logs trend-radar > debug.log 2>&1
```

---

#### Local

**Console output while running:**
```bash
python main.py
```

**Redirect to file:**
```bash
python main.py > output.log 2>&1
```

---

### Enable Debug Mode

**Increase log verbosity:**

Add to `config/config.yaml`:
```yaml
app:
  debug_mode: true
  log_level: "DEBUG"
```

Or set environment variable:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python main.py
```

---

### Test Mode (Dry Run)

**Run without sending notifications:**

```bash
python main.py --test-mode
```

Or in config:
```yaml
notification:
  enable_notification: false
```

This helps test keyword matching and data fetching without spam.

---

### Verify Configuration

**Validate YAML syntax:**
```bash
python -c "import yaml; print(yaml.safe_load(open('config/config.yaml')))"
```

**Check environment variables (Docker):**
```bash
docker exec trend-radar env | grep -E "ENABLE|REPORT|EMAIL|NTFY"
```

**Test webhook manually:**
- See [Check 5 under No Notifications](#check-5-test-webhook-directly)

---

### Check Network Connectivity

**Test API endpoint:**
```bash
curl https://newsnow.busiyi.world/api/data
```

Should return JSON data.

**Test with proxy:**
```bash
curl -x http://127.0.0.1:7890 https://newsnow.busiyi.world/api/data
```

---

### Clean State

**Sometimes old state causes issues. Reset:**

```bash
# Backup first
cp -r output/ output_backup/

# Clear old data
rm -rf output/*

# Clear push records (if using push windows)
rm -rf .push_history/

# Run fresh
python main.py
```

---

## Error Messages Reference

### Common Error Patterns

| Error Pattern | Meaning | Solution |
|---------------|---------|----------|
| `ConnectionError` | Can't reach API/webhook | Check network, proxy |
| `TimeoutError` | Request took too long | Increase timeout, check network |
| `AuthenticationError` | Wrong credentials | Verify tokens/passwords |
| `PermissionError` | Can't write to folder | Fix permissions |
| `KeyError` | Missing config field | Check config.yaml complete |
| `FileNotFoundError` | File missing | Verify file exists at path |
| `HTTPError 403` | Access denied | Check credentials, rate limits |
| `HTTPError 429` | Too many requests | Reduce frequency |
| `HTTPError 500` | Server error | Wait and retry, external issue |

---

### Specific Error Solutions

<details>
<summary><code>yaml.scanner.ScannerError</code></summary>

**Cause:** Invalid YAML syntax

**Fix:**
1. Check indentation (must use spaces, not tabs)
2. Quote URLs and special characters
3. Validate: https://www.yamllint.com/
</details>

<details>
<summary><code>ModuleNotFoundError: No module named 'requests'</code></summary>

**Cause:** Dependencies not installed

**Fix:**
```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><code>AttributeError: 'NoneType' object has no attribute</code></summary>

**Cause:** API returned no data or unexpected format

**Fix:**
1. Check API status: https://newsnow.busiyi.world/
2. Wait 10 minutes and retry
3. Check logs for which platform failed
</details>

<details>
<summary><code>ssl.SSLError</code></summary>

**Cause:** SSL/TLS connection issue

**Fix:**
1. Update Python SSL certificates
2. Try different SMTP port (587 vs 465)
3. Check system time is correct
</details>

<details>
<summary><code>UnicodeEncodeError</code></summary>

**Cause:** Encoding issue with special characters

**Fix:**
1. Ensure files saved as UTF-8
2. Check for unusual characters in config
3. Remove emoji or special symbols
</details>

---

## Getting Additional Help

### Before Asking for Help

**Prepare this information:**

1. **Environment:**
   - Deployment method: GitHub Actions / Docker / Local
   - Operating system and version
   - Python version (if local)
   - Docker version (if Docker)

2. **What you tried:**
   - Steps to reproduce
   - Configuration (redact sensitive data!)
   - Recent changes made

3. **Error evidence:**
   - Full error message
   - Relevant logs (last 50 lines)
   - Screenshots if applicable

4. **What you've checked:**
   - List troubleshooting steps already attempted
   - Results of each attempt

---

### How to Share Logs

**❌ Don't share raw logs with sensitive data!**

**✅ Redact before sharing:**

```bash
# Redact sensitive info
cat output.log | \
  sed 's/bot[0-9]*:[A-Za-z0-9_-]*/BOT_TOKEN_REDACTED/g' | \
  sed 's/[a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]*/EMAIL_REDACTED/g'
```

**Or manually replace:**
- Bot tokens → `BOT_TOKEN_REDACTED`
- Webhook URLs → `WEBHOOK_REDACTED`
- Email addresses → `EMAIL_REDACTED`
- API keys → `API_KEY_REDACTED`

---

### Where to Get Help

**📖 Documentation (Start here):**
- [Quick Start Guide](QUICKSTART.md)
- [Installation Guide](INSTALLATION.md)
- [Configuration Guide](CONFIGURATION.md)
- [Deployment Guide](DEPLOYMENT.md)
- [API Reference](API_REFERENCE.md)

**💬 GitHub Issues** (Bug reports, feature requests):
- Search existing issues first
- Use issue templates
- Include all info from "Before Asking for Help" above
- Link: https://github.com/sansan0/TrendRadar/issues

**🗣️ GitHub Discussions** (Questions, community help):
- General questions
- Configuration help
- Sharing tips and tricks
- Link: https://github.com/sansan0/TrendRadar/discussions

**📱 WeChat Official Account** (Chinese users):
- Quick Q&A in comments
- See [README](../README-EN.md) for QR code

---

### Creating a Good Bug Report

**Use this template:**

```markdown
**Environment:**
- Deployment: [GitHub Actions / Docker / Local]
- OS: [Windows 11 / Ubuntu 22.04 / macOS 14]
- Python: [3.10.5 / Docker image]

**Description:**
Clear description of the problem.

**Steps to Reproduce:**
1. Fork repository
2. Configure secrets
3. Run workflow
4. Error occurs

**Expected Behavior:**
What should happen.

**Actual Behavior:**
What actually happens.

**Error Logs:**
```
[Paste redacted logs here]
```

**Configuration:**
```yaml
# Relevant config (redact sensitive data)
notification:
  enable_notification: true
  # ...
```

**What I've Tried:**
- Checked secrets are set
- Verified config.yaml syntax
- Tested webhook manually - works
- Checked logs - see error above

**Additional Context:**
Any other relevant information.
```

---

### Quick Reference Card

**Print and keep handy:**

```
┌─────────────────────────────────────────────┐
│   TrendRadar Quick Troubleshooting Card     │
├─────────────────────────────────────────────┤
│                                             │
│ 🔍 CHECK LOGS FIRST:                        │
│  • GitHub: Actions → Run → crawl            │
│  • Docker: docker logs trend-radar          │
│  • Local: console output                    │
│                                             │
│ 🛠️ COMMON FIXES:                            │
│  • No notifications: Check secrets/config   │
│  • Actions not running: Enable workflows    │
│  • Docker won't start: Check config mount   │
│  • Empty data: Loosen keywords              │
│  • Email fails: Use app password            │
│  • Rate limited: Increase interval          │
│                                             │
│ 🧪 DEBUG COMMANDS:                          │
│  • Validate YAML:                           │
│    python -c "import yaml; yaml.safe_load(  │
│      open('config/config.yaml'))"           │
│                                             │
│  • Test webhook:                            │
│    curl -X POST "WEBHOOK_URL" -d '{...}'    │
│                                             │
│  • View Docker logs:                        │
│    docker logs --tail 100 trend-radar       │
│                                             │
│ 📚 DOCS:                                     │
│  docs/TROUBLESHOOTING.md (this file)        │
│  docs/CONFIGURATION.md                      │
│  docs/DEPLOYMENT.md                         │
│                                             │
│ 💬 GET HELP:                                 │
│  github.com/sansan0/TrendRadar/issues       │
│  github.com/sansan0/TrendRadar/discussions  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Success! 🎉

**Resolved your issue?** Consider:

- ⭐ **Star the repository** if TrendRadar helps you
- 📝 **Share your solution** in Discussions to help others
- 🐛 **Report any documentation gaps** so we can improve

---

[← Back to Configuration](CONFIGURATION.md) | [Next: API Reference →](API_REFERENCE.md)
