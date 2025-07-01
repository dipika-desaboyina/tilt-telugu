import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
from urllib.parse import urlparse
from datetime import datetime
import os

# fetch the script type
def detect_script(text):
    telugu_chars = re.findall(r'\p{Telugu}', text)
    latin_chars = re.findall(r'\p{Latin}', text)
    if len(telugu_chars) > 0 and len(latin_chars) > 0:
        return 'Code-mixed'
    elif len(telugu_chars) > 0:
        return 'Telugu'
    elif len(latin_chars) > 0:
        return 'Romanised'
    return 'Unknown'

# get vertical (limited categories)
def extract_vertical(url):
    path_parts = urlparse(url).path.strip('/').split('/')
    for part in path_parts:
        if part.lower() in ['national', 'state', 'business', 'sports', 'cinema', 'editorial', 'crime', 'health', 'tech', 'education', 'international','andhra-pradesh','telangana']:
            return part.capitalize()
    return 'General'

# sentence splitter by period 
# note - this doesn't work for acronyms  etc so we can try executing by <p> in the page body
def split_sentences(text):
    return re.split(r'[\n\r]+', text)

def scrape_news_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_div = soup.find('div', class_='article')  # this class needs to be updated for every website based on html structure


    if not article_div:
        print("article content not found.")
        return None

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
                'date_scraped': date_scraped,
                'source' : "bbc telugu"
            })

    return pd.DataFrame(data)

dirpath = r"/home/jellybun/Desktop/Telugu_Mixed_Quality_Web_Data/DevelopmentSpace/data_collection/"
os.chdir(dirpath)

scraped_data = []

if __name__ == "__main__":
    url_list = "bbc_telugu_urls.txt"

    with open(url_list) as source:
        urls = [line.strip() for line in source if line.strip()]
        for url in urls:
            df = scrape_news_article(url)  # make sure this function returns a pandas dataframe
            if df is not None and not df.empty:
                print(df.head())
                scraped_data.append(df)

    if scraped_data:
        full_df = pd.concat(scraped_data, ignore_index=True)
        full_df.to_csv("bbc_telugu_scraped.csv", index=False, encoding='utf-8-sig')
    else:
        print("No data scraped.")

