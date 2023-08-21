"""
Template to extract full text from arxiv.org.
"""

from .template_base import TemplateBase
from readability import Document
from pyquery import PyQuery as pq
from nltk.tokenize import sent_tokenize


class ArxivTemplate(TemplateBase):
    def get_title(self, raw_html):
        return Document(raw_html).title()

    def split_into_sections(self, raw_html):
        doc = Document(raw_html).summary()

        sections = []
        for section in pq(doc, parser='html_fragments'):
            text = pq(section).remove("a").text().split("\n")  # remove links to references
            for t in text:
                sections.append(sent_tokenize(t))  # split into sentences
        return sections
    
