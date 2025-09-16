import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load API keys from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_news_articles(topic):
    """Fetches news articles using the News API."""
    if not NEWS_API_KEY:
        print("Error: NEWS_API_KEY not found in .env file.")
        return []

    url = (f"https://newsapi.org/v2/everything?"
           f"q={topic}&sortBy=publishedAt&apiKey={NEWS_API_KEY}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        print(f"Found {len(articles)} articles on '{topic}'.\n")
        return articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_with_gemini(articles):
    """Analyzes news articles using the Gemini API."""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    # --- THIS LINE IS CHANGED ---
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    print("--- Analyzing News with Gemini ---")
    for article in articles[:3]:
        title = article.get('title', 'N/A')
        description = article.get('description', 'No description available.')

        print(f"\n-> Analyzing Article: {title}")

        prompt = (f"You are a neutral news fact-checker. Analyze the following news article."
                  f"Provide a brief, one-paragraph summary and then give your assessment of its likely credibility (e.g., 'Appears credible', 'Lacks sources', 'Potential bias')."
                  f"\n\nTitle: {title}\nDescription: {description}")

        try:
            response = model.generate_content(prompt)
            print("Gemini's Analysis:")
            print(response.text)
        except Exception as e:
            print(f"  Could not get analysis from Gemini: {e}")
        print("-" * 20)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    search_topic = "latest developments in Artificial Intelligence"

    list_of_articles = fetch_news_articles(search_topic)

    if list_of_articles:
        analyze_with_gemini(list_of_articles)
