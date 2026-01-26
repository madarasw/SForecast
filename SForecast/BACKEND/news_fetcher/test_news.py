from fetch_and_save_news import fetch_news_urls
from fetch_and_save_news import fetch_news_contents
from fetch_and_save_news import save_batch_to_db
from datetime import datetime, timedelta
import time

Dataset =  'Financial_news_dataset'
start_date = "2023-01-24"
end_date = "2023-01-31"
Macro_var = 'Inflation'

query = '("expected inflation" OR "CPI projection") AND ("higher than expected" OR "lower than expected")'

start_dt = datetime.strptime(start_date, "%Y-%m-%d")
end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

current = start_dt
while current <= end_dt:
    start_dt_formatted = current.strftime("%Y%m%d%H%M%S")
    end_dt_formatted = (current + timedelta(days=1) - timedelta(seconds=1)).strftime("%Y%m%d%H%M%S")

    print(f"--------------------------{start_dt_formatted},{end_dt_formatted}--------------------------")

    start_time = time.time()
    articles_without_contents = fetch_news_urls(start_dt_formatted, end_dt_formatted, query)
    articles_with_contents = fetch_news_contents(articles_without_contents)
    save_batch_to_db(articles_with_contents)
    end_time = time.time()

    elapsed = end_time - start_time
    if elapsed < 6:
        time.sleep(6 - elapsed)

    current += timedelta(days=1)