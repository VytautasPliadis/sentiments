import requests
from bs4 import BeautifulSoup
from translate import Translator


class LithuanianToEnglishTranslator:
    def __init__(self):
        self.translator = Translator(to_lang="en", from_lang="lt")

    def translate_list(self, lithuanian_words):
        english_words = []
        for word in lithuanian_words:
            translation = self.translator.translate(word)
            english_words.append(translation)
        return english_words


class SentenceTranslator:
    def __init__(self, source_lang="lt", target_lang="en"):
        self.translator = Translator
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate_sentence(self, sentence):
        translation = self.translator.translate(sentence, src=self.source_lang, dest=self.target_lang)
        return translation.text

    def translate_sentences(self, sentences):
        translated_sentences = []
        for sentence in sentences:
            translated_sentence = self.translate_sentence(sentence)
            translated_sentences.append(translated_sentence)
        return translated_sentences


class TitleScraper:
    def __init__(self, url_link, element1, element2=None):
        self.url_link = url_link
        self.element1 = element1
        self.element2 = element2
        self.title_list_en = []
        self.title_list_lt = []

    @staticmethod
    def clean_titles(input_text):
        try:
            cleaned_text = input_text.split(' / \n', 1)[1].split('\r', 1)[0].split('\n', 1)[0]
        except IndexError:
            cleaned_text = input_text.split('\r', 1)[0].split('\n', 1)[0]

        return cleaned_text

    def scrape_titles(self):
        source = requests.get(self.url_link).text
        soup = BeautifulSoup(source, 'html.parser')

        elements = soup.find_all(self.element1, self.element2)
        if not elements:
            elements = soup.select(self.element1)

        for element in elements:
            title_lt = self.clean_titles(element.get_text().strip())
            try:
                self.title_list_lt.append(title_lt.encode('latin-1').decode('utf-8', errors='ignore'))
            except:
                self.title_list_lt.append(title_lt)

    def get_10_titles(self):
        return self.title_list_lt[:10]

    def __str__(self):
        return "\n".join(self.title_list_lt[:10])


if __name__ == "__main__":
    # scraper_configs = [
    #     ('https://www.delfi.lt', '.CBarticleTitle'),
    #     ('https://www.15min.lt/', 'h4', 'vl-title item-no-front-style'),
    #     ('https://www .lrt.lt', 'h3')#('https://www.lrytas.lt/', 'h2')
    # ]
    # # Create and run scraper objects in a loop
    # for config in scraper_configs:
    #     scraper = TitleScraper(*config)
    #     scraper.scrape_titles()
    #     print(scraper)
    #     print('---')

    '''
        scraper = TitleScraper('https://www.lrt.lt', 'h3')
        scraper.scrape_titles()
        titles_to_translate = scraper.get_10_titles()
        print(titles_to_translate)
        
        lt_translator = LithuanianToEnglishTranslator()
        english_titles = lt_translator.translate_list(titles_to_translate)
        print(english_titles)
    '''

    scraper = TitleScraper('https://www.lrt.lt', 'h3')
    scraper.scrape_titles()
    titles_to_translate = scraper.get_10_titles()
    print(titles_to_translate)