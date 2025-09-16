import pathway as pw
import os
import requests
from dotenv import load_dotenv

def fetch_news_articles():
    load_dotenv()
    API_KEY = os.getenv("NEWS_API_KEY")
    topic = "Artificial Intelligence"
    url = (f"https://newsapi.org/v2/everything?"
           f"q={topic}&"
           f"sortBy=publishedAt&"
           f"apiKey={API_KEY}")
    
    try:
        response = requests.get(url)
        return response.json().get("articles", [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

list_of_articles = fetch_news_articles()

if list_of_articles:
    articles_table = pw.Table.from_rows(list_of_articles)

    final_table = articles_table.select(
        articles_table.title
    )

    pw.debug.show(final_table)
    pw.run()
else:
    print("Koi articles nahi mile, isliye pipeline run nahi ho rahi.")
