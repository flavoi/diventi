from bs4 import BeautifulSoup

from django.conf import settings

from diventi.core.utils import extract_diventi_content


def make_paper_toc_cards(paper_soup):
    """
        Extracts H1 and H2 elements from the page and writes 
        a list of cards with their relative subheadings.
    """
    toc = []
    title_dict = {}
    for title in paper_soup.find_all(['h1', 'h2']):
        title['id'] = title['data-usually-unique-id']
        
        if title.name == 'h1':
            # Main Headings will become card titles
            if title_dict:
                toc.append(title_dict)                
            parent_title_key = title.span.string
            title_dict = {
                parent_title_key : [
                    {
                        'string': title.span.string,
                        'anchor': title['id'],
                        'name': title.name,
                    }           
                ]
            }
        else:
            # Sub-headings nested into headings
            title_dict[parent_title_key].append(
                {
                    'string': title.span.string,
                    'anchor': title['id'],
                    'name': title.name,
                } 
            )
    toc.append(title_dict)
    return toc


def make_paper_toc_linear(paper_soup):
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


def make_paper_toc(paper_soup):
    """
        Activates our preferred toc.
    """
    return make_paper_toc_cards(paper_soup)


def render_diventi_snippets(paper_soup, diventi_universale_soup):
    """
        Substitutes paper links inside the main paper with
        linked contents in Diventi Universale.
    """
    paper_mentions = paper_soup.select('.mention-content') 
    for p in paper_mentions:    
        mentioned_uuid = p.get('data-mentionpadid', None)
        mentioned_href = p.get('href', None)
        if mentioned_uuid:
            mention = mentioned_uuid
        elif mentioned_href:
            mention = mentioned_href
        else:
            mention = None        
        if mention:
            diventi_title = extract_diventi_content(mention, diventi_universale_soup)
            if diventi_title:
                p.parent.parent.parent.replace_with(diventi_title)
