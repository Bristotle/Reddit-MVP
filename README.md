# 🚀 Reddit Lead Generation Agent (First Motion MVP)

An automated lead discovery tool designed to scan Reddit for high-intent keywords, classify them using OpenAI, and push qualified opportunities directly to an Airtable CRM.

## 🌟 Key Features
* **Keyword Monitoring:** Scans subreddits like `r/Entrepreneur` and `r/SaaS` for specific buyer-intent keywords.
* **AI Classification:** Uses OpenAI to filter out noise and identify actual business opportunities.
* **CRM Integration:** Automatically syncs leads to Airtable for immediate follow-up.
* **Slack Notifications:** Real-time alerts via Webhooks when a "hot" lead is discovered.

## 🏗️ Tech Stack
* **Language:** Python 3.x
* **Data Source:** Reddit JSON API
* **Intelligence:** OpenAI API (GPT-4o/3.5)
* **Storage:** Airtable API
* **Communication:** Slack Webhooks

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Bristotle/Reddit-MVP.git](https://github.com/Bristotle/Reddit-MVP.git)
```
2. **Install dependencies:**
   ```bash
   pip install requests python-dotenv openai
```
3. **Create a .env file in the root directory and add your keys:**
   ```bash
   AIRTABLE_TOKEN=your_token
AIRTABLE_BASE_ID=your_id
OPENAI_API_KEY=your_key
SLACK_WEBHOOK_URL=your_url 
```
