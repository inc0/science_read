import pytest
from templates.arxiv import ArxivTemplate


def test_arxiv():
    url =  "https://www.biorxiv.org/content/10.1101/2023.08.05.552127v1.full"
    template = ArxivTemplate(url)
    assert template.url == url

    title, sections = template.parse()

    assert sections[0] == ["Introduction"]
    assert sections[1][:2] == ["Nitrogen (N) is essential for plant growth and development.", "However, atmospheric N2 is relatively inert and cannot be directly utilized by most plants ()."]
    assert title == 'Mucilage produced by sorghum (Sorghum bicolor) aerial roots supports a nitrogen-fixing community | bioRxiv'