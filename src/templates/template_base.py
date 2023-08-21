import requests


class TemplateBase(object):
    def __init__(self, url):
        self.url = url

    def download(self):
        # TODO: this could also deal with pdf someday
        return requests.get(self.url).text

    def extract_raw_text(self, raw_html):
        raise NotImplementedError()

    def get_title(self, raw_html):
        raise NotImplementedError()

    def parse(self):
        """
        This function should return a tuple of title and list of sections.
        Each section is a list of sentences.
        """
        raw_html = self.download()
        return self.get_title(raw_html), self.split_into_sections(raw_html)
