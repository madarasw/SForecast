from news_fetcher.fetch_and_save_news import fetch_news
from manage_database.database_test import store_news_article

def run_pipeline(dataset, start_date, end_date, macro_var, query):

    print(dataset, start_date, end_date, macro_var, query)
    print('-----------------------------END-----------------------------')

    news_item = {
        "url": "https://www.bnnbloombewrergsssssttt.ca/india-s-rbi-may-lower-inflation-forecast-by-50-bps-says-citi-1.1869665",
        "url_mobile": "https://www.bnnbloosdfmbergsssssttt.ca/india-s-rbi-may-lower-inflation-forecast-by-50-bps-says-citi-1.1869665.amp.html",
        "title": "India RBI May Lower Inflation Forecast by 50 BPS , Says Citi",
        "seendate": "20230113T083000Z",
        "domain": "bnnbloomberg.ca",
        "language": "English",
        "geography": "Sri Lanka",
        "content": "Canada’s former foreign affairs says...",
        "fetch_date": "20230113T083000Z",
        "deviation": True
    }

    store_news_article(news_item)






