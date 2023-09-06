import requests
from nltk.sentiment import SentimentIntensityAnalyzer
from translate import Translator
from bs4 import BeautifulSoup
import streamlit as st
translator = Translator(to_lang="en", from_lang="lt")

#LT titles
source = requests.get('https://www.delfi.lt').text
soup = BeautifulSoup(source, 'html.parser')
elements = soup.select('.CBarticleTitle')

title_list_en = []
title_list_lt = []

for element in elements:
    title_lt = element.get_text()
    title_list_lt.append(title_lt)
    # title_en = translator.translate(title_lt)
    # title_list_en.append(title_en)

# with st.expander("Click to expand Delfi headlines"):
#     for index, title in enumerate(title_list_lt, start=1):
#         st.write(f'{index}. {title}')

title_list_en = translator.translate(title_list_lt)

#Sentiment analysis
analyzer = SentimentIntensityAnalyzer()
sentiment = analyzer.polarity_scores('.'.join(title_list_en))
print(sentiment['compound'])


# #EN titles
# source = requests.get('https://www.delfi.lt/en').text
# soup = BeautifulSoup(source, 'html.parser')
# # Find all elements with article titles
# article_titles = soup.find_all("div", class_="C-block-type-102-headline__content")
#
# # Extract and print the EN titles
# for title in article_titles:
#     title_text = title.find("a").text.strip()
#     print(title_text)