import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_article_links(base_url, section_url, num_articles=100):

    article_links = []
    page = 1
    len_in_page = [0]

    while len(article_links) < num_articles:
        response = requests.get(f"{base_url}{section_url}?page={page}")

        # print(response)

        soup = BeautifulSoup(response.content, 'html.parser')

        # print(soup.find_all('a', href=True))

        for a in soup.find_all('a', href=True):
            href = urljoin(base_url, a['href'])

            # print(href)

            if href.startswith('https://www.naukawpolsce.pl/aktualnosci/') and href not in article_links:
                article_links.append(href)
                if len(article_links) >= num_articles:
                    break

        len_in_page.append(len(article_links))

        # print(page + 1, len(article_links))

        # kończy pobieranie, gdy na stronie nie ma już więcej artykułów
        if len_in_page[page] - len_in_page[page-1] == 0:
            break
        page += 1

    return article_links


def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # tablica wszystkich paragrafów
    paragraphs = soup.find_all('p')

    # scala wszystkie parafrafy z tablicy w jeden artykuł
    article_text = ' '.join([p.get_text() for p in paragraphs])

    return article_text


def website_scraper(base_url, section_url, num_articles):
    articles = get_article_links(base_url, section_url, num_articles)
    articles_content = []

    for link in articles:
        content = get_article_content(link)
        articles_content.append(content)

    return articles_content


article_content = website_scraper("https://www.naukawpolsce.pl", "/kosmos", 100)

string_articles = [str(article) for article in article_content]

df = pd.DataFrame({'content': string_articles, 'label': [1 for i in range(len(string_articles))]})

df.to_csv('articles_pap.csv', index=False)
