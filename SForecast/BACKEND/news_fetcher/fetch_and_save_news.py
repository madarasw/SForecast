import requests
from newspaper import Article

import trafilatura
import requests


from tqdm import tqdm
from langdetect import detect
import psycopg2
from datetime import datetime
import hashlib

# ------------------ CONFIG ------------------
max_articles = 250
# --------------------------------------------
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


##################################### FETCH URlS #####################################
def fetch_from_gdelt(params):
    resp = requests.get(GDELT_URL, params=params)
    if resp.status_code != 200:
        raise Exception(f"GDELT API request failed: {resp.status_code}")
    data = resp.json()
    if "articles" not in data:
        return []
    return data["articles"]


def fetch_news_urls(start_date, end_date, query):
    params = {
        "query": query,
        "mode": "ArtList",
        "maxrecords": max_articles,
        "format": "json",
        "filter": (
            "lang:english "
            "domain:reuters.com,apnews.com,bbc.com,bloomberg.com,"
            "nytimes.com,theguardian.com,ft.com,washingtonpost.com,"
            "aljazeera.com,economist.com"
        ),
        "startdatetime": start_date,
        "enddatetime": end_date
    }

    articles= fetch_from_gdelt(params)
    print(f"Retrieved {len(articles)} article URLs.\nExtracting full content...")
    return articles

##################################### FETCH CONTENTS #####################################

def fetch_content(url):
    """Try to extract the main article text via newspaper3k"""
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text
    except Exception as e:
        print(f"Failed to extract: {url} ({e})")
        return ""

def fetch_news_contents(articles):
    enriched = []
    for art in tqdm(articles):
        url = art.get("url")
        if not url:
            continue

        text = fetch_content(url)
        try:
            if text and detect(text) == "en":  # keep only English content
                art["content"] = text
                enriched.append(art)
        except:
            pass
    return enriched


##################################### SAVE TO DATABASE #####################################

DEFAULT_DB_CONFIG = {
    "dbname": "SForecast_financial_news",
    "user": "postgres",
    "password": "mdr",
    "host": "localhost",
    "port": "5432"
}

# ---------------- DB CONNECTION ----------------
def get_db_connection(db_config=DEFAULT_DB_CONFIG):
    return psycopg2.connect(**db_config)


# ---------------- DATE PARSER ----------------
def parse_date(a_date):
    """
    Converts date from GDELT-style format: YYYYMMDDTHHMMSSZ
    """
    return datetime.strptime(a_date, "%Y%m%dT%H%M%SZ")

def insert_news_article(unique_id, conn, news_item):
    insert_query = """
    INSERT INTO public.all_news(
        id, url, url_mobile, title, published_at,
        domain, language, sourcecountry, socialimage, content
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (id) DO NOTHING;
    """

    published_at = parse_date(news_item["seendate"])

    with conn.cursor() as cur:
        cur.execute(
            insert_query,
            (
                unique_id,
                news_item["url"],
                news_item.get("url_mobile"),
                news_item["title"],
                published_at,
                news_item.get("domain"),
                news_item.get("language"),
                news_item.get("sourcecountry"),
                news_item.get("socialimage"),
                news_item["content"]
            )
        )
        conn.commit()


def store_news_article(news_item, conn):
    url = news_item['url']
    unique_id = hashlib.sha256(url.encode()).hexdigest()

    try:
        insert_news_article(str(unique_id), conn, news_item)
    except Exception as e:
        print(f"Failed to store article {url}: {e}")


def save_batch_to_db(articles):
    conn = get_db_connection()
    for news_item in articles:
        store_news_article(news_item, conn)
    print("saved to database successfully")
    conn.close()