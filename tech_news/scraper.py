# Requisito 1
import time
import requests
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    time.sleep(1)
    try:
        result = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
            )
        result.raise_for_status()
        return result.text
    except (requests.ReadTimeout, requests.HTTPError):
        return None


# Requisito 2
def scrape_novidades(html_content):
    return Selector(html_content).css(".entry-title a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    return Selector(html_content).css(".next::attr(href)").get()


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".entry-title::text").get().strip()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css("a.url::text").get()
    comments_count = selector.css(
        ".post-comments h5.title-block::text"
        ).get() or 0
    summary = selector.xpath("string(//p)").get().strip()
    tags = selector.css(".post-tags a::text").getall()
    category = selector.css(".meta-category span.label::text").get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": summary,
        "tags": tags,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com"
    noticias = []
    qnt_noticias = 0
    while qnt_noticias < amount:
        pagina = fetch(url)
        novidades = scrape_novidades(pagina)
        for link in novidades:
            noticia = scrape_noticia(fetch(link))
            noticias.append(noticia)
            qnt_noticias += 1
            if (qnt_noticias == amount):
                break
        url = scrape_next_page_link(pagina)

    create_news(noticias)
    return noticias
