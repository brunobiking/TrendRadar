# Configuration Guide

**⏱️ Time Estimate: 20-40 minutes for complete setup**

Comprehensive guide to configuring TrendRadar for your needs.

## Table of Contents
- [Configuration Overview](#configuration-overview)
- [Core Configuration (config.yaml)](#core-configuration-configyaml)
- [Notification Channels Setup](#notification-channels-setup)
- [Keyword Configuration](#keyword-configuration)
- [Advanced Configuration](#advanced-configuration)

---

## Configuration Overview

TrendRadar uses two main configuration files:

| File | Purpose | Format | Location |
|------|---------|--------|----------|
| `config/config.yaml` | Main settings | YAML | Core configuration |
| `config/frequency_words.txt` | Keywords | Plain text | Keyword filtering |

### Configuration Methods

**Method 1: Edit Files Directly** (Recommended for GitHub/Local)
- Edit `config/config.yaml` in your repository
- Commit changes to Git

**Method 2: GitHub Secrets** (Recommended for sensitive data)
- Store webhooks/tokens in Settings → Secrets
- Keeps credentials private

**Method 3: Environment Variables** (Best for Docker)
- Set in `.env` file or Docker environment
- Overrides `config.yaml` settings
- Perfect for NAS users

---

## Core Configuration (config.yaml)

### Application Settings

```yaml
app:
  version_check_url: "https://raw.githubusercontent.com/sansan0/TrendRadar/refs/heads/master/version"
  show_version_update: true
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `version_check_url` | URL | (GitHub URL) | Where to check for updates |
| `show_version_update` | boolean | `true` | Show update notifications |

**Recommended:** Keep defaults unless you fork and maintain your own version.

---

### Crawler Settings

```yaml
crawler:
  request_interval: 1000
  enable_crawler: true
  use_proxy: false
  default_proxy: "http://127.0.0.1:10086"
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `request_interval` | milliseconds | `1000` | Delay between API requests |
| `enable_crawler` | boolean | `true` | Enable/disable news crawling |
| `use_proxy` | boolean | `false` | Use proxy for requests |
| `default_proxy` | URL | (local proxy) | Proxy server URL |

**Tips:**
- **Increase `request_interval`** if you hit rate limits (try 2000-3000ms)
- **Use proxy** if accessing from restricted networks
- Set `enable_crawler: false` for testing notification setup only

---

### Report Mode

The most important setting - controls what and when news is pushed.

```yaml
report:
  mode: "daily"
  rank_threshold: 5
```

#### Mode Options

| Mode | When to Push | What to Push | Best For |
|------|--------------|--------------|----------|
| **`daily`** | Every execution | All matching news of the day | Comprehensive daily summaries |
| **`current`** | Every execution | Current top rankings | Real-time trending topics |
| **`incremental`** | Only when new items appear | Only new matching news | Avoiding duplicates |

#### Detailed Mode Explanations

<details>
<summary><b>📋 Daily Mode</b> - Comprehensive Summary</summary>

**How it works:**
- Collects all matching news from midnight to now
- Pushes complete summary on each execution
- Shows historical trend (first appearance → latest)

**Example use case:**
```
You run TrendRadar hourly.
At 10:00 AM, you get all AI news from 00:00-10:00.
At 11:00 AM, you get all AI news from 00:00-11:00 (includes previous + new).
```

**Best for:**
- Daily summary reports
- Comprehensive trend overview
- Understanding full day's activity

**Notification frequency:** High (every execution)

**Configuration:**
```yaml
report:
  mode: "daily"
  rank_threshold: 5  # Highlight top 5 rankings
```
</details>

<details>
<summary><b>📰 Current Mode</b> - Real-Time Rankings</summary>

**How it works:**
- Shows only what's trending RIGHT NOW
- Focuses on current top rankings
- Still includes "new items" section

**Example use case:**
```
You run TrendRadar hourly.
At 10:00 AM, you get what's trending NOW (current top 50).
At 11:00 AM, you get updated current top 50 (may be different).
```

**Best for:**
- Content creators needing hot topics
- Real-time market monitoring
- What's viral right now

**Notification frequency:** High (every execution)

**Configuration:**
```yaml
report:
  mode: "current"
  rank_threshold: 3  # Focus on top 3 only
```
</details>

<details>
<summary><b>📈 Incremental Mode</b> - New Items Only</summary>

**How it works:**
- Remembers what was already sent
- Only pushes NEW matching items
- Prevents duplicate notifications

**Example use case:**
```
You run TrendRadar every 30 min.
At 10:00 AM, "Tesla announces new model" appears → You get notified.
At 10:30 AM, same Tesla news still trending → No notification (already sent).
At 11:00 AM, "Tesla stock up 10%" appears → You get notified (new item).
```

**Best for:**
- High-frequency monitoring (every 10-30 min)
- Stock/crypto traders
- Breaking news alerts
- Avoiding notification spam

**Notification frequency:** Low (only when new)

**Configuration:**
```yaml
report:
  mode: "incremental"
  rank_threshold: 10  # Less important, all new items flagged anyway
```
</details>

#### rank_threshold

```yaml
report:
  rank_threshold: 5
```

**What it does:** News ranked ≤ this threshold appears in **bold red** in notifications.

**Examples:**
- `rank_threshold: 5` → Top 5 items highlighted
- `rank_threshold: 10` → Top 10 items highlighted
- `rank_threshold: 1` → Only #1 highlighted

**In notifications you'll see:**
```
✅ [Zhihu] AI chatbot breakthrough [**2**] - 09:15
   ↑ Bold and red (rank 2 ≤ threshold 5)

✅ [Baidu] AI conference announced [7] - 09:20
   ↑ Normal (rank 7 > threshold 5)
```

---

### Notification Settings

```yaml
notification:
  enable_notification: true
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enable_notification` | boolean | `true` | Master switch for all notifications |

**Note:** Email and ntfy notifications do not require batch splitting or special configuration.

**Use case for disabling:**
```yaml
notification:
  enable_notification: false  # Disable push, only generate HTML reports
```

---

### Push Time Window (Optional Feature)

Control WHEN notifications are sent to avoid disturbances.

```yaml
notification:
  push_window:
    enabled: false
    time_range:
      start: "08:00"
      end: "22:00"
    once_per_day: true
    push_record_retention_days: 7
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable time window control |
| `start` | HH:MM | `"20:00"` | Window start time (Beijing time) |
| `end` | HH:MM | `"22:00"` | Window end time (Beijing time) |
| `once_per_day` | boolean | `true` | Limit to one push per day |
| `push_record_retention_days` | integer | `7` | Days to keep push history |

#### Use Cases

<details>
<summary><b>Scenario 1: Work Hours Only</b></summary>

**Goal:** Only receive notifications during work hours (9 AM - 6 PM)

**Configuration:**
```yaml
push_window:
  enabled: true
  time_range:
    start: "09:00"
    end: "18:00"
  once_per_day: false  # Push every execution within window
```

**Behavior:**
- Crawler runs every hour
- Between 09:00-18:00: Notifications sent normally
- Between 18:00-09:00: No notifications (data still collected)
</details>

<details>
<summary><b>Scenario 2: Evening Summary Only</b></summary>

**Goal:** Get one daily summary between 8-10 PM

**Configuration:**
```yaml
push_window:
  enabled: true
  time_range:
    start: "20:00"
    end: "22:00"
  once_per_day: true  # Only once!
```

**Behavior:**
- Crawler runs every hour
- First execution between 20:00-22:00: Notification sent
- Subsequent executions same day: Skipped
- Next day after 20:00: Notification resumes
</details>

<details>
<summary><b>Scenario 3: Weekend Off</b></summary>

**Goal:** No notifications on weekends

**Note:** This requires cron schedule modification, not just push_window.

**Docker `.env`:**
```bash
# Run only Monday-Friday
CRON_SCHEDULE=0 * * * 1-5
```

**GitHub Actions `crawler.yml`:**
```yaml
schedule:
  - cron: "0 * * * 1-5"  # Weekdays only
```

Combine with push window for precise control.
</details>

**⚠️ Important Notes:**
- Time is **Beijing Time (UTC+8)**
- GitHub Actions has ±10 minute variance (not precise)
- For precise windows, use Docker/Local deployment
- Window only affects NOTIFICATIONS, crawler still runs

---

### Weight Configuration

Customize how TrendRadar scores and ranks news.

```yaml
weight:
  rank_weight: 0.6
  frequency_weight: 0.3
  hotness_weight: 0.1
```

**⚠️ Rule:** All three weights MUST sum to 1.0

#### Weight Explanations

| Weight | What It Measures | High Weight Effect |
|--------|------------------|-------------------|
| `rank_weight` | Original platform ranking | Prioritizes top-ranked news |
| `frequency_weight` | How often it appears | Prioritizes persistent topics |
| `hotness_weight` | Ranking quality over time | Prioritizes consistently high-ranked |

#### Algorithm Formula

```
Score = (rank_weight × rank_score) + 
        (frequency_weight × frequency_score) + 
        (hotness_weight × hotness_score)
```

Where:
- `rank_score` = 1 / (average rank across platforms)
- `frequency_score` = appearance count / max appearances
- `hotness_score` = 1 / (average rank over time)

#### Tuning Examples

<details>
<summary><b>Preset 1: Real-Time Trending (Default)</b></summary>

**Goal:** See what's TOP-RANKED right now

```yaml
weight:
  rank_weight: 0.6      # Strong focus on current rankings
  frequency_weight: 0.3  # Some importance on persistence
  hotness_weight: 0.1    # Minor consideration of quality
```

**Effect:**
- News at #1 on multiple platforms appears first
- Good for: Content creators, social media managers
- Example: "What's viral on Twitter RIGHT NOW?"
</details>

<details>
<summary><b>Preset 2: Deep Analysis</b></summary>

**Goal:** Find stories with staying power

```yaml
weight:
  rank_weight: 0.4      # Moderate ranking importance
  frequency_weight: 0.5  # Strong focus on persistence
  hotness_weight: 0.1    # Minor quality consideration
```

**Effect:**
- News appearing repeatedly over hours ranks higher
- Good for: Researchers, journalists, investors
- Example: "What story is developing throughout the day?"
</details>

<details>
<summary><b>Preset 3: Quality Focus</b></summary>

**Goal:** Find consistently high-quality trending topics

```yaml
weight:
  rank_weight: 0.5      # Balanced ranking focus
  frequency_weight: 0.2  # Less emphasis on repetition
  hotness_weight: 0.3    # Strong quality consideration
```

**Effect:**
- Prioritizes stories that are BOTH highly ranked AND persistent
- Good for: Premium content curation, editorial decisions
- Example: "What's truly important, not just loud?"
</details>

<details>
<summary><b>Preset 4: Breaking News</b></summary>

**Goal:** Catch new emerging stories

```yaml
weight:
  rank_weight: 0.8      # Maximum focus on current rank
  frequency_weight: 0.1  # Low persistence requirement
  hotness_weight: 0.1    # Low quality bar
```

**Effect:**
- Newly appearing high-ranked items immediately surface
- Good for: News desks, traders, breaking news alerts
- Example: "What just exploded onto the scene?"
</details>

**💡 Tuning Tips:**
1. Start with defaults
2. Run for a few days and observe results
3. Adjust in 0.1 increments
4. Re-evaluate after each change
5. Different use cases need different weights!

---

### Platforms Configuration

Customize which news sources to monitor.

```yaml
platforms:
  - id: "toutiao"
    name: "Toutiao"
  - id: "baidu"
    name: "Baidu Hot"
  - id: "zhihu"
    name: "Zhihu"
  # ... more platforms
```

#### Default Platforms (35+ sources)

**Chinese News Sources (11):**
- `toutiao` - Toutiao (今日头条)
- `baidu` - Baidu Hot Search (百度热搜)
- `wallstreetcn-hot` - Wallstreetcn (华尔街见闻)
- `thepaper` - The Paper (澎湃新闻)
- `bilibili-hot-search` - Bilibili (哔哩哔哩)
- `cls-hot` - Yicai (财联社)
- `ifeng` - Ifeng (凤凰网)
- `tieba` - Tieba (贴吧)
- `weibo` - Weibo (微博)
- `douyin` - Douyin (抖音)
- `zhihu` - Zhihu (知乎)

**USA Financial Sources (5):**
- `yahoo-finance-trending` - Yahoo Finance Trending
- `seeking-alpha` - Seeking Alpha Market News
- `benzinga` - Benzinga Real-time News
- `marketwatch` - MarketWatch Breaking News
- `finviz-news` - Finviz Market News

📖 **Detailed guide:** [USA Financial Sources Documentation](USA_FINANCIAL_SOURCES.md)

#### Add Custom Platforms

1. Visit [NewsNow website](https://newsnow.busiyi.world/) → Click "More"
2. Find your desired platform in the list
3. Check [source code](https://github.com/ourongxing/newsnow/tree/main/server/sources) for platform ID

**Example - Adding a new platform:**
```yaml
platforms:
  # Existing platforms...
  
  # Add new platform
  - id: "new-platform-id"
    name: "My Custom Source"
```

#### Remove Platforms

**Comment out unwanted platforms:**
```yaml
platforms:
  - id: "toutiao"
    name: "Toutiao"
  # - id: "baidu"        # Disabled
  #   name: "Baidu Hot"  # Disabled
  - id: "zhihu"
    name: "Zhihu"
```

**💡 Tip:** Reducing platforms decreases API calls and speeds up execution.

#### Platform-Specific Configuration

Some platforms support advanced options:

```yaml
platforms:
  - id: "yahoo-finance-trending"
    name: "Yahoo Finance Trending"
    enabled: true
    language: "en"
    category: "finance"
    config:
      data_type: ["trending", "gainers", "losers"]
```

| Setting | Type | Description |
|---------|------|-------------|
| `enabled` | boolean | Enable/disable this platform |
| `language` | string | Content language (en/zh) |
| `category` | string | Content category |
| `config` | object | Platform-specific options |

**See:** Community-shared configurations at [Issue #95](https://github.com/sansan0/TrendRadar/issues/95)

---

## Notification Channels Setup

Configure where to receive your trending news alerts.

### GitHub Secrets vs config.yaml

**⚠️ Security Best Practice:**

| Deployment | Webhooks/Tokens Storage | Reason |
|------------|------------------------|---------|
| **GitHub Fork** | GitHub Secrets (Settings → Secrets) | Config files are public! |
| **Local** | config.yaml | No security risk locally |
| **Docker** | .env file or environment variables | Better than yaml for containers |

**Never commit sensitive data to public repositories!**

---

### Email Notification

**⭐ Best for archiving** - Permanent record, team sharing, professional look.

⚠️ **Note:** Complex setup, requires email app password. Not recommended for beginners.

#### Supported Email Providers

| Provider | Domain | SMTP Server | Port | Encryption |
|----------|--------|-------------|------|------------|
| Gmail | gmail.com | smtp.gmail.com | 587 | TLS |
| QQ Mail | qq.com | smtp.qq.com | 465 | SSL |
| Outlook | outlook.com | smtp-mail.outlook.com | 587 | TLS |
| Hotmail | hotmail.com | smtp-mail.outlook.com | 587 | TLS |
| 163 Mail | 163.com | smtp.163.com | 465 | SSL |
| 126 Mail | 126.com | smtp.126.com | 465 | SSL |
| Sina Mail | sina.com | smtp.sina.com | 465 | SSL |
| Sohu Mail | sohu.com | smtp.sohu.com | 465 | SSL |

**Auto-detection:** For these providers, SMTP settings are automatic!

#### Step 1: Get App Password

**Different for each provider:**

<details>
<summary><b>Gmail</b></summary>

1. Go to Google Account → Security
2. Enable **2-Step Verification** (required!)
3. Go to **App Passwords**
4. Select app: Mail, device: Other → Name it "TrendRadar"
5. Copy the 16-character password

**What to use:**
- EMAIL_FROM: `youremail@gmail.com`
- EMAIL_PASSWORD: `abcd efgh ijkl mnop` (app password)
</details>

<details>
<summary><b>QQ Mail</b></summary>

1. Login QQ Mail web version
2. Settings → Account
3. Find **"POP3/SMTP Service"**
4. Click **"Enable"**
5. Send verification SMS
6. Copy the **authorization code** (16 characters)

**What to use:**
- EMAIL_FROM: `youremail@qq.com`
- EMAIL_PASSWORD: `abcdefghijklmnop` (authorization code, NOT QQ password)
</details>

<details>
<summary><b>163/126 Mail</b></summary>

1. Login 163/126 Mail web version
2. Settings → POP3/SMTP/IMAP
3. Enable **SMTP service**
4. Click **"Set authorization code"**
5. Complete verification
6. Copy authorization code

**What to use:**
- EMAIL_FROM: `youremail@163.com`
- EMAIL_PASSWORD: (authorization code)
</details>

<details>
<summary><b>Outlook/Hotmail</b></summary>

Similar to Gmail, requires app password:
1. Microsoft Account → Security
2. Advanced security options
3. App passwords → Create new
4. Copy the password

**What to use:**
- EMAIL_FROM: `youremail@outlook.com`
- EMAIL_PASSWORD: (app password)
</details>

#### Step 2: Configure

**GitHub Secrets (Minimum 3 required):**
| Secret Name | Required? | Example |
|------------|-----------|---------|
| `EMAIL_FROM` | ✅ Yes | `sender@gmail.com` |
| `EMAIL_PASSWORD` | ✅ Yes | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | ✅ Yes | `receiver@example.com` |
| `EMAIL_SMTP_SERVER` | ❌ Optional | `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | ❌ Optional | `587` |

**config.yaml:**
```yaml
notification:
  webhooks:
    email_from: "sender@gmail.com"
    email_password: "abcd efgh ijkl mnop"  # App password
    email_to: "receiver@example.com"
    email_smtp_server: ""  # Leave empty for auto-detect
    email_smtp_port: ""    # Leave empty for auto-detect
```

**Docker .env:**
```bash
EMAIL_FROM=sender@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=receiver@example.com
# EMAIL_SMTP_SERVER=  # Optional, leave commented for auto-detect
# EMAIL_SMTP_PORT=    # Optional, leave commented for auto-detect
```

#### Multiple Recipients

Separate with **commas** (English comma, no spaces):

```yaml
email_to: "person1@example.com,person2@example.com,person3@example.com"
```

Or in GitHub Secret:
```
person1@example.com,person2@example.com
```

**⚠️ Note:** All recipients see each other's addresses (CC-style).

#### Step 3: Test

**Python test script:**
```python
import smtplib
from email.mime.text import MIMEText

sender = "youremail@gmail.com"
password = "your-app-password"
receiver = "receiver@example.com"

msg = MIMEText("Test from TrendRadar")
msg['Subject'] = 'TrendRadar Test'
msg['From'] = sender
msg['To'] = receiver

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
server.send_message(msg)
server.quit()
print("Email sent successfully!")
```

#### Email Features

**HTML Formatted:**
- Beautiful visual layout (same as GitHub Pages)
- Mobile-responsive design
- Direct links to news sources
- Proper text formatting

**Archiving:**
- Permanent record in email inbox
- Searchable history
- Easy forwarding to team members

#### Common Issues

<details>
<summary>❌ "Authentication failed" error</summary>

**Common causes:**
1. Using actual password instead of app password
2. App password not enabled
3. 2-factor authentication not enabled (Gmail)
4. Wrong authorization code (QQ Mail)

**Solution:**
- Gmail: MUST use app password, not account password
- QQ Mail: MUST use authorization code (16 letters)
- Double-check you copied the password correctly (no spaces)
</details>

<details>
<summary>❌ "SMTP connection failed"</summary>

**Cause:** Wrong server or port.

**Solution:** Manually specify in config:
```yaml
email_smtp_server: "smtp.gmail.com"
email_smtp_port: "587"
```

Or try alternative port:
- TLS: Port 587
- SSL: Port 465
</details>

<details>
<summary>❌ Email sent but not received</summary>

**Check:**
1. Spam/junk folder
2. Recipient address correct
3. Sender reputation (new Gmail accounts may be flagged)

**Solution:**
- Mark TrendRadar emails as "Not Spam"
- Add sender to contacts
- Check email filters
</details>

---

### ntfy

**⭐ Privacy-focused, open-source, self-hostable**

Perfect for users who want:
- ✅ No account registration
- ✅ Open-source (MIT License)
- ✅ Self-hosting option
- ✅ Cross-platform (iOS, Android, Desktop, Web)

#### Method 1: Free Public Service (Easiest)

**Step 1: Choose Topic Name**

Topic name acts as your "password" - make it hard to guess!

**Good examples:**
```
trendradar-john-8492
news-alerts-mary-2847
trending-alex-9134
```

**Bad examples (too easy to guess):**
```
news
alerts
trending
trendradar
```

**Rules:**
- Only letters, numbers, underscores, hyphens
- No spaces or special characters
- No Chinese/non-ASCII characters

**Step 2: Download App**

- **Android:** [Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy) | [F-Droid](https://f-droid.org/packages/io.heckel.ntfy/)
- **iOS:** [App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
- **Desktop/Web:** Visit [ntfy.sh](https://ntfy.sh)

**Step 3: Subscribe to Topic**

1. Open app
2. Click **"+"** or **"Subscribe to topic"**
3. Enter your topic name (e.g., `trendradar-john-8492`)
4. Click Subscribe

**Step 4: Configure**

**GitHub Secrets:**
| Secret Name | Value |
|------------|-------|
| `NTFY_TOPIC` | `trendradar-john-8492` |

Optional (for self-hosting):
| Secret Name | Value |
|------------|-------|
| `NTFY_SERVER_URL` | `https://ntfy.sh` |
| `NTFY_TOKEN` | (leave empty) |

**config.yaml:**
```yaml
notification:
  webhooks:
    ntfy_server_url: "https://ntfy.sh"
    ntfy_topic: "trendradar-john-8492"
    ntfy_token: ""  # Leave empty for public service
```

**Docker .env:**
```bash
NTFY_SERVER_URL=https://ntfy.sh
NTFY_TOPIC=trendradar-john-8492
# NTFY_TOKEN=  # Leave commented for public service
```

**Step 5: Test**

```bash
curl -d "Test from TrendRadar" ntfy.sh/trendradar-john-8492
```

Expected: Notification appears on your device!

**Public service limits:**
- 250 messages/day (enough for hourly TrendRadar)
- 5 MB attachment size
- No message retention

---

#### Method 2: Self-Hosted (Advanced)

For complete privacy and control.

**Step 1: Deploy ntfy Server**

**Docker (Easiest):**
```bash
docker run -d \
  --name ntfy \
  -p 80:80 \
  -v /var/cache/ntfy:/var/cache/ntfy \
  binwiederhier/ntfy \
  serve --cache-file /var/cache/ntfy/cache.db
```

**Your server:** `http://your-server-ip`

**Step 2: (Optional) Enable Authentication**

Edit ntfy config for private topics:

```yaml
# /etc/ntfy/server.yml
auth-file: /var/cache/ntfy/auth.db
auth-default-access: deny-all
```

Create user:
```bash
docker exec ntfy ntfy user add myuser
docker exec ntfy ntfy access myuser mytopic rw
```

Generate token:
```bash
docker exec ntfy ntfy token add myuser
```

**Step 3: Configure TrendRadar**

```yaml
notification:
  webhooks:
    ntfy_server_url: "http://your-server-ip"
    ntfy_topic: "trendradar"
    ntfy_token: "tk_your_token_here"  # Only if auth enabled
```

**Step 4: Subscribe in App**

1. Open ntfy app
2. Settings → "Use another server"
3. Enter: `http://your-server-ip`
4. Subscribe to topic: `trendradar`
5. (If auth enabled) Enter username and token

---

#### Common Issues

<details>
<summary>❌ Not receiving notifications</summary>

**Check:**
1. Topic name matches exactly (case-sensitive!)
2. App is subscribed to correct topic
3. Test with curl command (see above)
4. Check app notification permissions (iOS/Android settings)

**Debug:**
- Visit `https://ntfy.sh/trendradar-your-topic` in browser
- Should see "Connected" and test notification appear there too
</details>

<details>
<summary>❌ "401 Unauthorized" with self-hosted</summary>

**Cause:** Authentication required but token not provided or wrong.

**Solution:**
1. Verify token is correct
2. Check ntfy server config allows access
3. Test access with curl:
   ```bash
   curl -H "Authorization: Bearer tk_your_token" \
     -d "Test" your-server/trendradar
   ```
</details>

<details>
<summary>❌ Topic name guessable?</summary>

**Security analysis:**

With rate limiting (1 req/sec) and 64 possible characters:
- 10 random chars = 64^10 = 1.15 × 10^18 possibilities
- At 1 req/sec, would take 36 billion years to brute force

**Best practices:**
- Use 12+ character random topic names
- Combine words with numbers: `trendradar-john-8492`
- For sensitive data, use self-hosted with authentication

**Note:** ntfy itself doesn't encrypt messages. For true privacy, self-host with HTTPS + authentication.
</details>

---

## Keyword Configuration

Control which news reaches you through precise keyword filtering.

### File Location

```
config/frequency_words.txt
```

### Syntax Overview

Three keyword types:

| Syntax | Symbol | Purpose | Example |
|--------|--------|---------|---------|
| **Normal** | None | Basic matching | `Apple` |
| **Required** | `+` | Must include | `+phone` |
| **Filter** | `!` | Exclude | `!advertisement` |

**+ Groups:** Empty lines separate independent groups.

---

### Basic Syntax Examples

#### 1. Normal Keywords

Match ANY of these words:

```txt
Apple
Tesla
Bitcoin
```

**Matches:**
- ✅ "Apple announces new iPhone"
- ✅ "Tesla stock rises"
- ✅ "Bitcoin reaches new high"
- ❌ "Microsoft launches Surface" (no keyword match)

---

#### 2. Required Keywords (+)

Must include BOTH normal keyword AND required keyword:

```txt
Apple
Tesla
+phone
```

**Matches:**
- ✅ "Apple iPhone 15 launched" (has "Apple" + "phone")
- ✅ "Tesla's phone project revealed" (has "Tesla" + "phone")
- ❌ "Apple M3 chip released" (has "Apple" but no "phone")
- ❌ "Samsung phone unveiled" (has "phone" but no "Apple" or "Tesla")

**Rule:** (Normal keyword) AND (Required keyword)

---

#### 3. Filter Keywords (!)

Exclude if filter word present:

```txt
Apple
Tesla
!advertisement
!rumor
```

**Matches:**
- ✅ "Apple revenue report released"
- ❌ "Apple advertisement campaign launched" (contains "advertisement")
- ❌ "Tesla merger rumor surfaces" (contains "rumor")

**Priority:** Filter words have HIGHEST priority - excludes even if other keywords match.

---

### Group Feature

Empty lines separate groups - each group independently counted and ranked.

#### Example Configuration

```txt
iPhone
Huawei
Samsung
+launch

A-shares
Stock Market
Shanghai Index
+surge
!prediction

World Cup
Olympics
+medal
```

#### Group Behavior

**Group 1 - Phone Launches:**
```txt
iPhone
Huawei
Samsung
+launch
```

- Must have: (iPhone OR Huawei OR Samsung) AND "launch"
- ✅ "iPhone 15 launch event today"
- ✅ "Huawei flagship launch postponed"
- ❌ "iPhone sales hit record" (no "launch")

**Group 2 - Stock Market:**
```txt
A-shares
Stock Market
Shanghai Index
+surge
!prediction
```

- Must have: (A-shares OR Stock Market OR Shanghai Index) AND "surge"
- Must NOT have: "prediction"
- ✅ "A-shares surge 5% today"
- ✅ "Stock Market surge on good news"
- ❌ "Analysts predict A-shares surge" (has "prediction")

**Group 3 - Sports:**
```txt
World Cup
Olympics
+medal
```

- Must have: (World Cup OR Olympics) AND "medal"
- ✅ "World Cup golden medal winners"
- ✅ "Olympics medal count updated"
- ❌ "World Cup schedule released" (no "medal")

---

### Advanced Patterns

#### Pattern 1: Broad to Narrow

**Strategy:** Start broad, add filters as needed.

**Iteration 1 - Too broad:**
```txt
AI
```
Result: Gets 100+ AI news items, too much noise.

**Iteration 2 - Add required words:**
```txt
AI
+breakthrough
+release
```
Result: Only AI news with "breakthrough" or "release" - better!

**Iteration 3 - Add filters:**
```txt
AI
+breakthrough
+release
!advertisement
!course
!training
```
Result: AI breakthroughs, excluding ads and training courses - perfect!

---

#### Pattern 2: Multiple Topics

**Separate interests into groups:**

```txt
# Technology
AI
Machine Learning
ChatGPT
OpenAI
Claude

# Finance
Bitcoin
Cryptocurrency
Stock Market
Nasdaq
S&P 500

# Sports
NBA
World Cup
Olympics
Tennis
!betting
!gambling
```

Each group ranks independently - you see top items from each interest area.

---

#### Pattern 3: Specific Events

**Monitor specific ongoing events:**

```txt
# iPhone 16 Launch
iPhone 16
+launch
+price
+feature
+release date

# US Election
Presidential
Election
+poll
+debate
+results
!prediction
!analysis
```

---

### Priority Ordering

Keywords at the top have higher weight in scoring.

**Example - If you care more about Apple:**

```txt
# High priority
Apple
iPhone
iPad

# Medium priority
Tesla
SpaceX

# Low priority
Samsung
Google
```

When multiple keywords match, top keywords score higher.

---

### Best Practices

#### ✅ DO:

1. **Start simple:** Begin with 5-10 normal keywords
2. **Test and refine:** Run for a few days, see what you get
3. **Use groups:** Separate different interests
4. **Add filters gradually:** Only when you see unwanted content
5. **Update regularly:** Adjust based on your changing interests

#### ❌ DON'T:

1. **Over-complicate:** Too many filters = miss important news
2. **Too many required words:** Makes matching too strict
3. **Ignore grouping:** All keywords in one group = poor organization
4. **Set and forget:** Review and update monthly

---

### Example Configurations

#### Use Case 1: Tech Investor

```txt
# Stock Monitoring
AAPL
TSLA
NVDA
MSFT
+stock
+earnings
+revenue
!rumor

# Tech News
Apple
Tesla
NVIDIA
Microsoft
+announcement
+release
!advertisement

# Market Indicators
Nasdaq
S&P 500
Dow Jones
+surge
+drop
+close
```

---

#### Use Case 2: Content Creator

```txt
# Viral Topics
trending
viral
popular
+social media
+video

# Tech Launches
iPhone
Android
+launch
+reveal
+announcement

# Entertainment
Netflix
Disney
HBO
+series
+movie
+release
!renewal
!cancelled
```

---

#### Use Case 3: News Enthusiast

```txt
# Everything (no filters)
```

**⚠️ Note:** Empty file = receive ALL trending news (not recommended, very high volume).

Better approach - use broad keywords:
```txt
news
breaking
important
major
significant
```

---

### Testing Keywords

#### Test locally:

```bash
# Run with test keywords
python main.py

# Check output
cat output/$(date +%Y年%m月%d日)/txt/*.txt
```

#### Evaluate results:

1. Too many matches? → Add filters or required words
2. Too few matches? → Remove filters, add more normal keywords
3. Wrong content? → Adjust keyword specificity
4. Missing important news? → Broaden keywords

---

### Empty File Behavior

If `frequency_words.txt` is **empty**:
- ✅ All trending news pushed (from all 35+ platforms)
- ⚠️ Very high volume (100+ items per hour)
- 🐛 May exceed notification platform limits

**Workaround for "everything":**
```yaml
# In config.yaml, reduce platforms:
platforms:
  - id: "zhihu"
    name: "Zhihu"
  - id: "weibo"
    name: "Weibo"
  # Comment out others...
```

---

## Advanced Configuration

### Environment Variable Override

**New in v3.0.5:** Override config.yaml with environment variables.

Perfect for:
- ✅ Docker/NAS users (hard to edit YAML files)
- ✅ Multiple environments (dev/prod)
- ✅ CI/CD pipelines

#### Available Overrides

| Environment Variable | config.yaml Path | Example |
|---------------------|------------------|---------|
| `ENABLE_CRAWLER` | `crawler.enable_crawler` | `true` |
| `ENABLE_NOTIFICATION` | `notification.enable_notification` | `true` |
| `REPORT_MODE` | `report.mode` | `daily` |
| `PUSH_WINDOW_ENABLED` | `notification.push_window.enabled` | `false` |
| `PUSH_WINDOW_START` | `notification.push_window.time_range.start` | `08:00` |
| `PUSH_WINDOW_END` | `notification.push_window.time_range.end` | `22:00` |
| All webhook variables | `notification.webhooks.*` | (URLs/tokens) |

#### Priority

```
Environment Variables > config.yaml > Defaults
```

#### Example - Docker

**Scenario:** NAS user can't easily edit YAML, wants to change mode.

**Solution in .env:**
```bash
REPORT_MODE=incremental
PUSH_WINDOW_ENABLED=true
PUSH_WINDOW_START=09:00
PUSH_WINDOW_END=18:00
```

Restart container:
```bash
docker-compose restart
```

Changes apply immediately, no YAML editing needed!

---

### Configuration Validation

Before first run, validate your configuration:

**Check YAML syntax:**
```bash
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

Expected: No output = valid YAML.

**Check required fields:**
```bash
python main.py --validate-config
```

Expected: "✅ Configuration valid"

**Common YAML errors:**

<details>
<summary>❌ "mapping values are not allowed here"</summary>

**Cause:** Incorrect indentation or missing quotes.

**Fix:**
```yaml
# Bad
webhook_url: https://example.com?key=value

# Good (use quotes for URLs with special chars)
webhook_url: "https://example.com?key=value"
```
</details>

<details>
<summary>❌ "could not find expected ':'"</summary>

**Cause:** Missing colon or incorrect structure.

**Fix:**
```yaml
# Bad
notification
  enable_notification: true

# Good
notification:
  enable_notification: true
```
</details>

---

### Backup Configuration

Before making major changes:

```bash
# Backup config
cp config/config.yaml config/config.yaml.backup
cp config/frequency_words.txt config/frequency_words.txt.backup

# Restore if needed
cp config/config.yaml.backup config/config.yaml
```

---

## Next Steps

After configuration:

### 📊 Test & Monitor
1. **[Run test execution](DEPLOYMENT.md#verify-deployment)** - Ensure everything works
2. **[Check logs](TROUBLESHOOTING.md#debug-steps)** - Monitor for errors
3. **[Review notifications](QUICKSTART.md#first-notification-test)** - Verify content quality

### 🎯 Fine-Tune
1. **[Adjust keywords](#keyword-configuration)** - Based on results
2. **[Tune weights](#weight-configuration)** - Match your use case
3. **[Optimize schedule](DEPLOYMENT.md#configure-workflow-schedule)** - Balance freshness vs API limits

### 🚀 Advanced Features
1. **[Enable GitHub Pages](DEPLOYMENT.md#enable-github-pages-optional)** - Web interface
2. **[Set up AI analysis](../README-Cherry-Studio.md)** - Natural language queries
3. **[Add multiple channels](#notification-channels-setup)** - Redundancy

---

## Getting Help

### 📚 Documentation
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common configuration issues
- **[Deployment Guide](DEPLOYMENT.md)** - How to run TrendRadar
- **[API Reference](API_REFERENCE.md)** - Technical details

### 💬 Community Support
- **[GitHub Issues](https://github.com/sansan0/TrendRadar/issues)** - Report problems
- **[Discussions](https://github.com/sansan0/TrendRadar/discussions)** - Ask questions
- **[Example Configurations](https://github.com/sansan0/TrendRadar/issues/95)** - Community-shared setups

---

[← Back to Installation](INSTALLATION.md) | [Next: Troubleshooting Guide →](TROUBLESHOOTING.md)
