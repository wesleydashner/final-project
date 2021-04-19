import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_news_theonion():
    
    # url definition
    url = "https://www.theonion.com"
    
    # Request
    r1 = requests.get(url)
    r1.status_code

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    # Soup creation
    soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
    coverpage_news = soup1.find_all('h3', class_='fc-item__title')
    len(coverpage_news)
    
    number_of_articles = 5

    # Empty lists for content, links and titles
    news_contents = []
    list_links = []
    list_titles = []
    list_subjects = []
    list_dates = []

    for n in np.arange(0, number_of_articles):

        # We need to ignore "live" pages since they are not articles
        if "live" in coverpage_news[n].find('a')['href']:  
            continue

        # Getting the link of the article
        link = coverpage_news[n].find('a')['href']
        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        # Getting Date
        date = coverpage_news[n].find('date').get_text()
        list_dates.append(date)

        # Getting Subject
        subject = "News"
        list_subjects.append(subject)

        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all('div', class_='content__article-body from-content-api js-article__body')
        x = body[0].find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        news_contents.append(final_article)

    # df_features
    df_features = pd.DataFrame(
         {'title': list_titles,
          'text': news_contents,
          'subject': list_subjects,
          'date': list_dates
        })

    
    return (df_features)

    df = get_news_theonion()