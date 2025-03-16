"""
    Title: Newsletter
    Author: Bartosz Bohdziewicz
"""

import json
import requests as req
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

# Stałe #
URL: str = "https://tvn24.pl/"
NEWS_FILE: str = "news.json"
DELAY: int = 60

# Funkcje #
def get_old_news(file_name: str) -> dict:
    try:
        json_file = open(file_name, "r")
    except FileNotFoundError:
        return {
            "title": [],
            "url": [],
            "time": [],
            "summary": [],
        }
        
    content = json.load(json_file)
    json_file.close()

    return content

def save_news(file_name: str, content: dict) -> None:
    with open(file_name, "w") as json_file:
        json.dump(content, json_file)

def get_news(url: str) -> None:
    response: req.Response
    website: BeautifulSoup
    article_title: str
    article_url: str
    running: bool
    news: dict
    time: str

    news = get_old_news(NEWS_FILE)

    running = True
    while running:
        response = req.get(URL)
        time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        website = BeautifulSoup(response.text, "html.parser")

        for article_box in website.find_all("div", class_="teaser-wrapper")[0:1]:

            try:
                article_title = article_box.article.a['title'][11:]
                article_url = article_box.article.a['href']
            except KeyError:
                continue
            except TypeError:
                continue
            
            if not article_title in news['title']:
                subpage_response = req.get(article_url)
                subpage_soup = BeautifulSoup(subpage_response.text, "html.parser")
                try:
                    content = subpage_soup.find("div", class_="article-story-content").find_all("p")
                except AttributeError:
                    continue
                text = " ".join([paragraph.string for paragraph in content if not paragraph.string is None])
                

                news["title"].append(article_title)
                news["url"].append(article_url)
                news["time"].append(time)
                
        save_news(NEWS_FILE, news)

        # co minutę sprawdzaj wiadomości od nowa
        sleep(DELAY)

        # running = False

def main() -> None:
    get_news(URL)
        
# Wywołanie programu #
if __name__ == "__main__":
    main()