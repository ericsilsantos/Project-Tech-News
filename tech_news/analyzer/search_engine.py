from datetime import datetime
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    news = search_news({"title": {"$regex": title, "$options": "i"}})
    list_news = [(new["title"], new["url"]) for new in news]
    return list_news


# Requisito 7
def search_by_date(date):
    try:
        date_format = datetime.fromisoformat(date).strftime("%d/%m/%Y")
        news = search_news({"timestamp": {"$regex": date_format}})
        list_news = [(new["title"], new["url"]) for new in news]
        return list_news
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    news = search_news({"tags": {"$regex": tag, "$options": "i"}})
    list_news = [(new["title"], new["url"]) for new in news]
    return list_news


# Requisito 9
def search_by_category(category):
    news = search_news({"category": {"$regex": category, "$options": "i"}})
    list_news = [(new["title"], new["url"]) for new in news]
    return list_news
