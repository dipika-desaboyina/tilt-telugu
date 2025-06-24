import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import time

# regular expression to find urls : href="(.*?)" 

# --- Detect script type ---
def detect_script(text):
    telugu_chars = re.findall(r'\p{Telugu}', text)
    latin_chars = re.findall(r'\p{Latin}', text)
    if telugu_chars and latin_chars:
        return 'Code-mixed'
    elif telugu_chars:
        return 'Telugu'
    elif latin_chars:
        return 'Romanised'
    return 'Unknown'

# --- Extract vertical/category from URL ---
def extract_vertical(url):
    path_parts = urlparse(url).path.strip('/').split('/')
    for part in path_parts:
        if part.lower() in ['national', 'state', 'business', 'sports', 'cinema', 'editorial', 'crime', 'health', 'tech', 'education', 'international', 'andhra-pradesh', 'telangana']:
            return part.capitalize()
    return 'General'

# --- Split into sentences (simple rule-based) ---
def split_sentences(text):
    return re.split(r'[।.!?]', text)

# --- Scrape a single article URL ---
def scrape_eenadu_article(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_div = soup.find('div', class_='clearfix')

        if not article_div:
            return []

        paragraphs = article_div.find_all(['p', 'span'])
        article_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        sentences = split_sentences(article_text)

        date_scraped = datetime.now().strftime('%Y-%m-%d')
        vertical = extract_vertical(url)

        data = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                script_type = detect_script(sentence)
                data.append({
                    'text': sentence,
                    'script_type': script_type,
                    'vertical': vertical,
                    'source_url': url,
                    'date_scraped': date_scraped
                })
        return data
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return []


# --- Example usage ---
if __name__ == "__main__":
    # Example Eenadu article (update this with actual links you want to scrape)
    url = 'https://www.eenadu.net/movies/new-updates'  # Replace with real URL
    df = scrape_eenadu_article(url)

    if df is not None:
        print(df.head())
        df.to_csv("eenadu_scraped_data3.csv", index=False, encoding='utf-8-sig')
        print("✅ Data saved to eenadu_scraped_data.csv")
