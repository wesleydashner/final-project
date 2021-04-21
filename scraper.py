import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re


def get_news_FOX():
    # url definition
    url = "https://www.foxnews.com"

    # Request
    r1 = requests.get(url)
    r1.status_code

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    # Soup creation
    soup1 = BeautifulSoup(coverpage, 'html.parser')
    # News identification
    coverpage_news = soup1.find_all('h2', class_="title")
    print(len(coverpage_news))


    passable_news = []
    for n in np.arange(0,len(coverpage_news)):
        link = coverpage_news[n].find('a')['href']
        if link[0:10] != "https://vi":
            passable_news.append(link)

    number_of_articles = 10
    print(passable_news)
    # Empty lists for content, links and titles
    news_contents = []
    list_links = []
    list_titles = []
    list_subjects = []
    list_dates = []

    for n in np.arange(0, number_of_articles):

        # Getting the link of the article
        link = passable_news[n]
        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        # Getting Date
        date = "4/20/2021"
        list_dates.append(date)

        # Getting Subject
        subject = "Political News"
        list_subjects.append(subject)

        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html.parser')
        body = soup_article.find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(body)):
            paragraph = body[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        # Removing special characters
        final_article = re.sub("\\xa0", "", final_article)

        news_contents.append(final_article)

    # df_features
    df_features = pd.DataFrame(
        {'title': list_titles,
         'text': news_contents,
         'subject': list_subjects,
         'date': list_dates
         })

    return df_features


df = get_news_FOX()

print(df.head)

df.to_csv(r'/Users/CSUser/Documents/CS_5830/Final_Project/final-project/data/FOXNews_articles.csv', index=False)