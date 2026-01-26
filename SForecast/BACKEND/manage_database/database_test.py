import psycopg2
from datetime import datetime


# ---------------- DEFAULT DB CONFIG ----------------
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
def parse_published_date(seendate):
    """
    Converts date from GDELT-style format: YYYYMMDDTHHMMSSZ
    """
    return datetime.strptime(seendate, "%Y%m%dT%H%M%SZ")


# ---------------- INSERT NEWS RECORD ----------------
def insert_news_article(conn, news_item):
    insert_query = """
    INSERT INTO public.news_articles (
        url, url_mobile, title, published_at,
        domain, language, geography, content, fetch_date, deviation
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (url, fetch_date)
    DO UPDATE SET
        title = EXCLUDED.title,
        content = EXCLUDED.content,
        deviation = EXCLUDED.deviation,
        fetch_date = EXCLUDED.fetch_date;
    """

    published_at = parse_published_date(news_item["seendate"])

    with conn.cursor() as cur:
        cur.execute(
            insert_query,
            (
                news_item["url"],
                news_item.get("url_mobile"),
                news_item["title"],
                published_at,
                news_item.get("domain"),
                news_item.get("language"),
                news_item.get("geography"),
                news_item["content"],
                parse_published_date(news_item["fetch_date"]),
                news_item.get("deviation", False)
            )
        )
        conn.commit()


# ---------------- MAIN WRAPPER FUNCTION ----------------
def store_news_article(news_item, db_config=DEFAULT_DB_CONFIG):
    """
    One-call function:
    - connects to DB
    - ensures table exists
    - inserts article
    - closes connection
    """
    conn = get_db_connection(db_config)
    try:
        insert_news_article(conn, news_item)
        print("✅ News article stored successfully")
    finally:
        conn.close()

'''

news_item = {
        "url": "https://www.bnnbdfdfloocmbedfrsdg.ca/india-s-rbi-may-lower-inflation-forecast-by-50-bps-says-citi-1.1869665",
        "url_mobile": "https://www.bdfdfdxfdfnnbloomberg.ca/india-sf-rbi-may-lower-inflation-forecast-by-50-bps-says-citi-1.1869665.amp.html",
        "title": "India RBI May Lower Inflatiodfn Forecast bfy 50 BPS , Says Citi",
        "seendate": "20230113T083000Z",
        "domain": "bnnblooffmberg.ca",
        "language": "English",
        "geography": "Canada",
        "content": "Canadaf’s former foreign affairs says...",
        "fetch_date": "20230113T083000Z",
        "deviation": True
}

store_news_article(news_item)

'''