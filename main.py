import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
load_dotenv() # This tells Python to look at your .env file

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

import requests
from openai import OpenAI
import json
import time

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
headers = {"User-Agent": "FirstMotion_MVP_Bot/6.0"}

# --- 2. THE HUNTING GROUND ---
target_subreddits = ["Entrepreneur", "bigseo", "SaaS"]
target_keywords = ["seo", "ai", "search", "b2b", "marketing", "software", "saas", "geo", "aeo"]

print("🚀 Waking up the FirstMotion Bot (Powered by OpenAI)...\n")

airtable_endpoint = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
airtable_headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

for subreddit in target_subreddits:
    print(f"🔍 Scanning r/{subreddit} for top leads...")
    
    reddit_url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=3"
    
    response = requests.get(reddit_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        
        for post in posts:
            post_data = post['data']
            
            if not post_data.get('stickied'):
                title = post_data.get('title', '')
                snippet = post_data.get('selftext', '')[:600]
                url = f"https://www.reddit.com{post_data.get('permalink')}"
                
                text_to_check = (title + " " + snippet).lower()
                if any(keyword in text_to_check for keyword in target_keywords):
                    print(f"🎯 Target Acquired: {title[:40]}...")

                    # --- 3. THE OPENAI BRAIN ---
                    prompt = f"""
                    Analyze this Reddit post to see if it's a good opportunity to engage.
                    
                    Title: {title}
                    Content: {snippet}

                    Respond ONLY with a valid JSON object in this exact format:
                    {{
                        "score": 8,
                        "intent": "<A 3-word summary of what the user wants>",
                        "sentiment": "<1 word describing their emotion>",
                        "draft_1": "<A helpful, friendly reply answering their question>",
                        "draft_2": "<A helpful reply that softly mentions our agency FirstMotion>"
                    }}
                    """
                    
                    try:
                        ai_response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            response_format={ "type": "json_object" },
                            messages=[
                                {"role": "system", "content": "You are an expert AI engagement strategist for a marketing agency named FirstMotion. FirstMotion specializes in AI Search Optimization, GEO, and B2B SaaS growth. You output pure JSON."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        raw_json = ai_response.choices[0].message.content
                        ai_data = json.loads(raw_json)
                        
                        score = ai_data.get("score", 0)
                        intent = ai_data.get("intent", "Unknown")
                        sentiment = ai_data.get("sentiment", "Neutral")
                        draft_1 = ai_data.get("draft_1", "Drafting failed.")
                        draft_2 = ai_data.get("draft_2", "Drafting failed.")
                    except Exception as e:
                        print(f"⚠️ AI hiccuped: {e}")
                        time.sleep(3) 
                        continue

                    # --- 4. PUSH TO AIRTABLE ---
                    record_data = {
                        "records": [{
                            "fields": {
                                "Post Title": title,
                                "Subreddit": subreddit,
                                "URL": url,
                                "Content Snippet": snippet,
                                "Opportunity Score": int(score),
                                "Intent": intent,
                                "Sentiment": sentiment,
                                "Status": "Drafted",
                                "AI Drafted 1": draft_1,  
                                "AI Drafted 2": draft_2   
                            }
                        }]
                    }

                    at_response = requests.post(airtable_endpoint, json=record_data, headers=airtable_headers)
                    if at_response.status_code == 200:
                        print(f"   📥 Saved to Airtable!")
                        
                        # --- 5. SEND THE SLACK ALERT ---
                        slack_message = {
                            "text": f"🚨 *New Lead Scored: {score}/10*\n*Subreddit:* r/{subreddit}\n*Title:* {title}\n*Intent:* {intent} | *Sentiment:* {sentiment}\n<{url}|Click here to view on Reddit>\n_Drafts are waiting in Airtable!_"
                        }
                        slack_response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
                        
                        if slack_response.status_code == 200:
                            print(f"   🔔 Slack Alert Sent!")
                        else:
                            print(f"   ❌ Slack Alert Failed: {slack_response.text}")
                            
                    else:
                        print(f"   ❌ Failed to save to Airtable. Error: {at_response.text}")
                    
                    # Just a tiny 3-second pause to be polite to Reddit/Airtable
                    time.sleep(3) 
                        
        time.sleep(2) 
    else:
        print(f"❌ Error pulling from r/{subreddit}. Status: {response.status_code}")

print("🎉 OpenAI Sweep Complete! We are ready for the demo.")