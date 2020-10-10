from bs4 import BeautifulSoup

from django.conf import settings

from diventi.core.utils import extract_diventi_content


def make_paper_toc(paper_soup):
    """
        Extracts H1 and H2 elements from the page and writes 
        a list of titles with their relative ids.
    """
    toc = []
    for title in paper_soup.find_all(['h1', 'h2']):
        title['id'] = title['data-usually-unique-id']
        toc.append(
            { 
                'string': title.span.string,
                'anchor': title['id'],
                'name': title.name,
            }
        )
    return toc


def render_diventi_snippets(paper_soup, diventi_universale_soup):
    """
        Substitutes paper links inside the main paper with
        linked conteents in Diventi Universale.
    """
    paper_mentions = paper_soup.select('.mention-content') 
    for p in paper_mentions:
        mentioned_text = p['data-mentiontext']
        mentioned_uuid = p['data-mentionpadid']
        diventi_title = extract_diventi_content(mentioned_uuid, diventi_universale_soup)
        if diventi_title:
            p.parent.parent.replace_with(diventi_title)

