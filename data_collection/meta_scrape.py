import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
from datetime import datetime
from urllib.parse import urlparse
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Detect Telugu, Romanised, or Code-mixed script
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

# Guess category from URL
def extract_vertical(url):
    path_parts = urlparse(url).path.strip('/').split('/')
    for part in path_parts:
        if part.lower() in ['national', 'state', 'business', 'sports', 'cinema', 'editorial', 'crime', 'health', 'tech', 'education', 'international', 'andhra-pradesh', 'telangana']:
            return part.capitalize()
    return 'General'

# Extract and label all meta content
def scrape_meta_all(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    meta_tags = soup.find_all('meta')

    labeled_texts = []
    for tag in meta_tags:
        content = tag.get('content', '')
        content = content.strip()
        if content:
            script_type = detect_script(content)
            labeled_texts.append((content, script_type))

    if not labeled_texts:
        return None

    date_scraped = datetime.now().strftime('%Y-%m-%d')
    vertical = extract_vertical(url)

    return pd.DataFrame([{
        'text': text,
        'script_type': script_type,
        'vertical': vertical,
        'source_url': url,
        'date_scraped': date_scraped,
        'source': 'BBC Telugu',
    } for text, script_type in labeled_texts])

# Main runner
if __name__ == "__main__":
    input_file = "bbc_telugu_urls.txt"
    output_file = "bbc_telugu_meta_scraped_labeled.csv"
    scraped = []

    if not os.path.exists(input_file):
        print(f"[ERROR] URL list '{input_file}' not found.")
        exit()

    with open(input_file) as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"[INFO] Scraping {len(urls)} URLs")

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Processing: {url}")
        df = scrape_meta_all(url)
        if df is not None:
            scraped.append(df)
        else:
            print(f"[SKIPPED] No meta content in: {url}")

    if scraped:
        final_df = pd.concat(scraped, ignore_index=True)
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"[SUCCESS] Saved to {output_file}")
    else:
        print("[INFO] No meta data scraped.")
