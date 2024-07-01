import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from textproc import *


def get_article_links(base_url, section_url, num_articles=100):

    # print('Trwa pobieranie: ', section_url)

    # Zaczynamy od pustej listy artykułów i 1. strony wyszukiwarki
    article_links = []
    startpage = 102
    page = 1 + startpage

    # tablica pokazująca na i-tym miejscu, ile artykułów zostało pobrane włącznie z i-tą stroną
    len_in_page = [0]

    # Dodaję adresy artykułów do czasu, aż będzie tam określona liczbą.
    # Jeśli chcę więcej artykułów, niż jest ich na stronie, to pobieram wszystkie.
    while len(article_links) < num_articles:

        # Biorę dostęp ze strony naukawpolsce.pl/nazwa_sekcji/?page=numer_strony.
        # Przeglądam od najnowszych artykułów.
        response = requests.get(f"{base_url}{section_url}?page={page}")

        # print(response)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Przeglądam wszystkie artykuły danej stronie.
        for a in soup.find_all('a', href=True):
            href = urljoin(base_url, a['href'])

            # print(href)

            # Sprawdzam, czy prefiks jest odpowiedni i czy link jest już w zbiorze artykułów?
            # Bez wskazania prefiksu, pobierałoby różne strony, w tym strony zewnętrzne i inne podstrony papu.
            if href.startswith('https://www.naukawpolsce.pl/aktualnosci/') and href not in article_links:
                article_links.append(href)

                # Przerywa program, jeśli jest już wystarczająca liczba artykułów.
                if len(article_links) >= num_articles:
                    break

        len_in_page.append(len(article_links))

        # print(page + 1, len(article_links))

        # kończy pobieranie, gdy na stronie nie ma już nowego artykułu
        if len_in_page[page - startpage] - len_in_page[page - 1 - startpage] == 0:
            break
        page += 1

    return article_links


def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # tablica wszystkich paragrafów
    paragraphs = soup.find_all('p')

    # scala wszystkie paragrafy z tablicy w jeden artykuł
    article_text = ' '.join([p.get_text() for p in paragraphs])

    return article_text


def website_scraper(base_url, section, num_articles):
    section_url = "/" + section

    articles = get_article_links(base_url, section_url, num_articles)
    articles_content = []

    for link in articles:
        content = get_article_content(link)
        articles_content.append(content)
    return articles_content


def save_articles(base_url, section, num):
    article_content = website_scraper(base_url, section, num)
    string_articles = [str(article) for article in article_content]
    df = pd.DataFrame({'content': string_articles, 'label': [section for i in range(len(string_articles))]})
    df.to_csv(str(section) + str(len(string_articles)) + '.csv', index=False)


'''
save_articles('https://www.naukawpolsce.pl', 'historia-i-kultura', 2200)
save_articles('https://www.naukawpolsce.pl', 'kosmos', 220)
save_articles('https://www.naukawpolsce.pl', 'czlowiek', 220)
save_articles('https://www.naukawpolsce.pl', 'zdrowie', 220)
save_articles('https://www.naukawpolsce.pl', 'zycie', 220)
save_articles('https://www.naukawpolsce.pl', 'technologia', 220)
save_articles('https://www.naukawpolsce.pl', 'ziemia', 150)
save_articles('https://www.naukawpolsce.pl', 'materia-i-energia', 150)


df2 = pd.concat([pd.read_csv("czlowiek100.csv"),
                pd.read_csv("historia-i-kultura100.csv"),
                pd.read_csv("zycie100.csv"),
                pd.read_csv("kosmos100.csv"),
                pd.read_csv("technologia100.csv"),
                pd.read_csv("zdrowie100.csv"),
                pd.read_csv("materia-i-energia100.csv"),
                pd.read_csv("ziemia100.csv")],
                ignore_index=True)

df2.to_csv('articles_test.csv', index=False)

print(df2)

'''

