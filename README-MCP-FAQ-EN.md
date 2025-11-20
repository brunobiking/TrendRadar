# TrendRadar MCP Tool Usage Q&A

> AI Query Guide - How to Use the News Trend Analysis Tool Through Conversation

## ⚙️ Default Settings (Important!)

The following optimization strategies are used by default, mainly to save AI token consumption:

| Default Setting | Description | How to Adjust |
| --------------- | ----------- | ------------- |
| **Result Limit** | Returns 50 news items by default | Say "return top 10" or "give me 100 items" in conversation |
| **Time Range** | Queries today's data by default | Say "query yesterday", "last week" or "January 1 to 7" |
| **URL Links** | Does not return links by default (saves ~160 tokens/item) | Say "need links" or "include URLs" |
| **Keyword List** | Does not use frequency_words.txt to filter news by default | Only used when calling "trending topics" tool |

**⚠️ Important:** The choice of AI model directly affects tool invocation accuracy - smarter AI leads to more accurate calls. When you remove the above restrictions, such as expanding from today's query to a week's query, first you need to have a week's data locally, and second, token consumption may multiply (why "may"? For example, if I query and analyze 'Apple' trend over the last week, but there aren't many Apple news during that week, token consumption might actually be quite low).

**💡 Tip:** When you say "last 7 days", AI will automatically calculate the corresponding date range (e.g., 2025-10-18 to 2025-10-25) and pass it to the tool.


## 💰 AI Models

Below I use **[SiliconFlow](https://cloud.siliconflow.cn)** platform as an example, which offers many large models to choose from. During the development and testing of this project, I used this platform for extensive functional testing and validation.

### 📊 Registration Method Comparison

| Registration Method | Direct Registration Without Referral | Registration With Referral Link |
|:---:|:---:|:---:|
| Registration Link | [siliconflow.cn](https://cloud.siliconflow.cn) | [Referral Link](https://cloud.siliconflow.cn/i/fqnyVaIU) |
| Free Credits | 0 tokens | **20 million tokens** (≈14 CNY) |
| Extra Benefits | ❌ | ✅ Referrer also gets 20 million tokens |

> 💡 **Tip**: The above gift credits should allow you to make **200+ queries**


### 🚀 Quick Start

#### 1️⃣ Register and Get API Key

1. Complete registration using the link above
2. Visit [API Key Management Page](https://cloud.siliconflow.cn/me/account/ak)
3. Click "Create New API Key"
4. Copy the generated key (keep it safe)

#### 2️⃣ Configure in Cherry Studio

1. Open **Cherry Studio**
2. Go to "Model Service" settings
3. Find "SiliconFlow"
4. Paste the copied key into the **[API Key]** input box
5. Make sure the checkbox in the upper right corner shows **green** when enabled ✅

---

### ✨ Configuration Complete!

Now you can start using this project and enjoy stable, fast AI services!

After testing a query, immediately check [SiliconFlow Billing](https://cloud.siliconflow.cn/me/bills) to see the consumption for that query and have an estimate in mind.


## Basic Queries

### Q1: How to view the latest news?

**You can ask:**

- "Show me the latest news"
- "Query today's trending news"
- "Get the latest 10 news items from Zhihu and Weibo"
- "View latest news, need to include links"

**Tool called:** `get_latest_news`

**Tool return behavior:**

- MCP tool returns the latest 50 news items from all platforms to AI
- Does not include URL links (saves tokens)

**AI display behavior (important):**

- ⚠️ **AI typically auto-summarizes**, only showing some news (e.g., TOP 10-20 items)
- ✅ If you want to see all 50 items, you need to explicitly request: "Display all news" or "List all 50 items completely"
- 💡 This is the natural behavior of the AI model, not a tool limitation

**Can be adjusted:**

- Specify platform: e.g., "only from Zhihu"
- Adjust quantity: e.g., "return top 20"
- Include links: e.g., "need links"
- **Request full display**: e.g., "Display all, don't summarize"

---

### Q2: How to query news from a specific date?

**You can ask:**

- "Query yesterday's news"
- "Look at Zhihu news from 3 days ago"
- "What news was there on 2025-10-10"
- "News from last Monday"
- "Show me the latest news" (automatically queries today)

**Tool called:** `get_news_by_date`

**Supported date formats:**

- Relative dates: today, yesterday, day before yesterday, 3 days ago
- Week days: last Monday, this Wednesday, last monday
- Absolute dates: 2025-10-10, October 10

**Tool return behavior:**

- Automatically queries today when no date specified (saves tokens)
- MCP tool returns 50 news items from all platforms to AI
- Does not include URL links

**AI display behavior (important):**

- ⚠️ **AI typically auto-summarizes**, only showing some news (e.g., TOP 10-20 items)
- ✅ If you want to see all, you need to explicitly request: "Display all news, don't summarize"

---

### Q3: How to view the frequency statistics of topics I follow?

**You can ask:**

- "How many times did my followed keywords appear today"
- "See which keywords in my followed list are most popular"
- "Count the frequency of followed keywords in frequency_words.txt"

**Tool called:** `get_trending_topics`

**Important note:**

- This tool **does not** automatically extract news hotspots
- Instead, it counts your **personal followed keywords** set in `config/frequency_words.txt`
- This is a **customizable** list where you can add keywords based on your interests

---

## Search & Retrieval

### Q4: How to search for news containing specific keywords?

**You can ask:**

- "Search for news containing 'artificial intelligence'"
- "Find reports about 'Tesla price cut'"
- "Search Musk-related news, return top 20"
- "Find news about 'iPhone 16' from the last 7 days"
- "Find 'Tesla' related news from January 1 to 7, 2025"
- "Find the link to the news about 'iPhone 16 release'"

**Tool called:** `search_news`

**Tool return behavior:**

- Uses keyword pattern search
- Searches today's data by default
- AI automatically converts relative times like "last 7 days", "last week" to specific date ranges
- MCP tool returns up to 50 results to AI
- Does not include URL links

**AI display behavior (important):**

- ⚠️ **AI typically auto-summarizes**, only showing some search results
- ✅ If you want to see all, you need to explicitly request: "Display all search results"

**Can be adjusted:**

- Specify time range:
  - Relative way: "Search from the last week" (AI auto-calculates dates)
  - Absolute dates: "Search from January 1 to 7, 2025"
- Specify platform: e.g., "only search Zhihu"
- Adjust sorting: e.g., "sort by weight"
- Include links: e.g., "need links"

**Example conversation:**

```
User: Search for news about "artificial intelligence breakthrough" from the last 7 days
AI: (auto-calculates: date_range={"start": "2025-10-18", "end": "2025-10-25"})

User: Find "Tesla" reports from January 2025
AI: (date_range={"start": "2025-01-01", "end": "2025-01-31"})
```

---

### Q5: How to find related historical news?

**You can ask:**

- "Find news related to 'artificial intelligence breakthrough' from yesterday"
- "Search last week's historical reports about 'Tesla'"
- "Find news related to 'ChatGPT' from last month"
- "Look for historical news related to 'iPhone launch event'"

**Tool called:** `search_related_news_history`

**Tool return behavior:**

- Searches yesterday's data
- Similarity threshold 0.4
- MCP tool returns up to 50 results to AI
- Does not include URL links

**AI display behavior (important):**

- ⚠️ **AI typically auto-summarizes**, only showing some related news
- ✅ If you want to see all, you need to explicitly request: "Display all related news"

---

## Trend Analysis

### Q6: How to analyze the trend of a topic's popularity?

**You can ask:**

- "Analyze the popularity trend of 'artificial intelligence' over the last week"
- "See if 'Tesla' topic is a flash in the pan or a sustained hotspot"
- "Detect which topics suddenly went viral today"
- "Predict potential hot topics coming next"
- "Analyze the life cycle of 'Bitcoin' in December 2024"

**Tool called:** `analyze_topic_trend`

**Tool return behavior:**

- Supports multiple analysis modes: popularity trend, life cycle, anomaly detection, prediction
- AI automatically converts relative times like "last week" to specific date ranges
- Analyzes last 7 days of data by default
- Statistics by day granularity

**AI display behavior:**

- Usually displays trend analysis results and charts
- AI may summarize key findings

**Example conversation:**

```
User: Analyze the life cycle of 'artificial intelligence' over the last week
AI: (auto-calculates: date_range={"start": "2025-10-18", "end": "2025-10-25"})

User: See if 'Bitcoin' in December 2024 was a flash in the pan or sustained hotspot
AI: (date_range={"start": "2024-12-01", "end": "2024-12-31"})
```

---

## Data Insights

### Q7: How to compare different platforms' attention to a topic?

**You can ask:**

- "Compare different platforms' attention to 'artificial intelligence' topic"
- "See which platform updates most frequently"
- "Analyze which keywords often appear together"

**Tool called:** `analyze_data_insights`

**Three insight modes:**

| Mode | Function | Example Question |
| ---- | -------- | ---------------- |
| **Platform Comparison** | Compare platform attention | "Compare platforms' attention to 'AI'" |
| **Activity Statistics** | Count platform publishing frequency | "See which platform updates most frequently" |
| **Keyword Co-occurrence** | Analyze keyword associations | "Which keywords often appear together" |

**Tool return behavior:**

- Platform comparison mode
- Analyzes today's data
- Keyword co-occurrence minimum frequency 3 times

**AI display behavior:**

- Usually displays analysis results and statistical data
- AI may summarize insight findings

---

## Sentiment Analysis

### Q8: How to analyze the sentiment tendency of news?

**You can ask:**

- "Analyze today's news sentiment tendency"
- "See if news related to 'Tesla' is positive or negative"
- "Analyze sentiment attitudes of different platforms toward 'artificial intelligence'"
- "Look at the sentiment tendency for 'Bitcoin' over a week, select top 20 most important items"

**Tool called:** `analyze_sentiment`

**Tool return behavior:**

- Analyzes today's data
- MCP tool returns up to 50 news items to AI
- Sorts by weight (prioritizes important news)
- Does not include URL links

**AI display behavior (important):**

- ⚠️ This tool returns **AI prompts**, not direct sentiment analysis results
- AI generates sentiment analysis report based on prompts
- Usually displays sentiment distribution, key findings, and representative news

**Can be adjusted:**

- Specify topic: e.g., "about 'Tesla'"
- Specify time: e.g., "last week"
- Adjust quantity: e.g., "return top 20"

---

### Q9: How to find similar news reports?

**You can ask:**

- "Find news similar to 'Tesla price cut'"
- "Search for similar reports about iPhone launch"
- "See if there are reports similar to this news"
- "Find similar news, need links"

**Tool called:** `find_similar_news`

**Tool return behavior:**

- Similarity threshold 0.6
- MCP tool returns up to 50 results to AI
- Does not include URL links

**AI display behavior (important):**

- ⚠️ **AI typically auto-summarizes**, only showing some similar news
- ✅ If you want to see all, you need to explicitly request: "Display all similar news"

---

### Q10: How to generate daily or weekly hotspot summaries?

**You can ask:**

- "Generate today's news summary report"
- "Give me a summary of this week's hotspots"
- "Generate news analysis report for the past 7 days"

**Tool called:** `generate_summary_report`

**Report types:**

- Daily summary: Summarizes the day's hot news
- Weekly summary: Summarizes the week's hot trends

---

## System Management

### Q11: How to view system configuration?

**You can ask:**

- "View current system configuration"
- "Display configuration file content"
- "What platforms are available?"
- "What is the current weight configuration?"

**Tool called:** `get_current_config`

**Can query:**

- Available platform list
- Crawler configuration (request interval, timeout settings)
- Weight configuration (ranking weight, frequency weight)
- Notification configuration (DingTalk, WeChat)

---

### Q12: How to check system running status?

**You can ask:**

- "Check system status"
- "Is the system running normally?"
- "When was the last crawl?"
- "How many days of historical data are there?"

**Tool called:** `get_system_status`

**Return information:**

- System version and status
- Last crawl time
- Historical data days
- Health check results

---

### Q13: How to manually trigger crawl tasks?

**You can ask:**

- "Please crawl current Toutiao news" (temporary query)
- "Help me fetch the latest news from Zhihu and Weibo and save" (persistent)
- "Trigger a crawl and save data" (persistent)
- "Get real-time data from 36Kr but don't save" (temporary query)

**Tool called:** `trigger_crawl`

**Two modes:**

| Mode | Purpose | Example |
| ---- | ------- | ------- |
| **Temporary Crawl** | Only returns data without saving | "Crawl Toutiao news" |
| **Persistent Crawl** | Save to output folder | "Fetch and save Zhihu news" |

**Tool return behavior:**

- Temporary crawl mode (does not save)
- Crawls all platforms
- Does not include URL links

**AI display behavior (important):**

- ⚠️ **AI typically summarizes crawl results**, only showing some news
- ✅ If you want to see all, you need to explicitly request: "Display all crawled news"

**Can be adjusted:**

- Specify platform: e.g., "only crawl Zhihu"
- Save data: say "and save" or "save locally"
- Include links: say "need links"

---

## 💡 Usage Tips

### 1. How to make AI display all data instead of auto-summarizing?

**Background**: Sometimes AI will automatically summarize data and only show partial content, even when the tool returns complete 50 items of data.

**If AI still summarizes, you can**:

- **Method 1 - Explicit request**: "Please display all news, don't summarize"
- **Method 2 - Specify quantity**: "Display all 50 news items"
- **Method 3 - Question behavior**: "Why only show 15 items? I want to see all"
- **Method 4 - Preemptive statement**: "Query today's news, display all results completely"

**Note**: AI may still adjust display method based on context.


### 2. How to combine multiple tools?

**Example: Deep analysis of a topic**

1. First search: "Search for news related to 'artificial intelligence'"
2. Then analyze trend: "Analyze the popularity trend of 'artificial intelligence'"
3. Finally sentiment analysis: "Analyze the sentiment tendency of 'artificial intelligence' news"

**Example: Track an event**

1. View latest: "Query today's news about 'iPhone'"
2. Find history: "Find historical news related to 'iPhone' from last week"
3. Find similar reports: "Find news similar to 'iPhone launch event'"
