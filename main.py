import requests
from bs4 import BeautifulSoup
from translate import Translator

translator = Translator(to_lang="en", from_lang="lt")


class TitleScraper():
    def __init__(self, url_link, element1, element2=None):
        self.url_link = url_link
        self.element1 = element1
        self.element2 = element2
        self.title_list_en = []
        self.title_list_lt = []

    @staticmethod
    def clean_titles(input_text):
        try:
            cleaned_text = input_text.split(' / \n', 1)[1].split('\r', 1)[0].split('\n\n', 1)[0].split('\n', 1)[0]
        except IndexError:
            cleaned_text = input_text.split('\r', 1)[0].split('\n\n', 1)[0].split('\n', 1)[0]

        return cleaned_text


    def scrape_titles(self):
        source = requests.get(self.url_link).text
        soup = BeautifulSoup(source, 'html.parser')

        elements = soup.find_all(self.element1, self.element2)
        if not elements:
            elements = soup.select(self.element1)

        for element in elements:
            title_lt = self.clean_titles(element.get_text().strip())
            self.title_list_lt.append(title_lt)
        # print(self.title_list_lt)

    def get_10_titles(self):
        return self.title_list_lt[:10]

    def __str__(self):
        return "\n".join(self.title_list_lt[:10])


if __name__ == "__main__":
    scraper_configs = [
        ('https://www.delfi.lt', '.CBarticleTitle'),
        ('https://www.15min.lt/', 'h4', 'vl-title item-no-front-style'),
        ('https://www.vz.lt/', 'h2'),
        ('https://www.lrytas.lt/', 'h2')
    ]
    # Create and run scraper objects in a loop
    for config in scraper_configs:
        scraper = TitleScraper(*config)
        scraper.scrape_titles()
        print(scraper)


    # #LT titles
    # source = requests.get('https://www.delfi.lt').text
    # soup = BeautifulSoup(source, 'html.parser')
    # elements = soup.select('.CBarticleTitle')
    #
    # for element in elements:
    #     title_lt = element.get_text()
    #     title_list_lt.append(title_lt)
    # title_en = translator.translate(title_lt)
    # title_list_en.append(title_en)
    #
    # with st.expander("Click to expand Delfi headlines"):
    #     for index, title in enumerate(title_list_lt, start=1):
    #         st.write(f'{index}. {title}')
    #
    # title_list_en = translator.translate(title_list_lt)
    #
    # Sentiment analysis
    # analyzer = SentimentIntensityAnalyzer()
    # sentiment = analyzer.polarity_scores('.'.join(title_list_en))
    # print(sentiment['compound'])
    #
    # #EN titles
    # source = requests.get('https://www.delfi.lt/en').text
    # soup = BeautifulSoup(source, 'html.parser')
    # # Find all elements with article titles
    # article_titles = soup.find_all("div", class_="C-block-type-102-headline__content")
    #
    #
    # # Extract and print the EN titles
    # for title in article_titles:
    #     title_text = title.find("a").text.strip()
    #     print(title_text)
