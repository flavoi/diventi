import requests, json, dropbox
from bs4 import BeautifulSoup

from django.conf import settings


def get_dropbox_paper_soup(paper_id):
    """
        Connects to dropbox API and export the Paper's content into memory
    """
    url = "https://content.dropboxapi.com/2/files/export"
    headers = {
        "Authorization": "Bearer {}".format(settings.DROPBOX_ACCESS_TOKEN),
        "Dropbox-API-Arg": "{{\"path\":\"{}\"}}".format(paper_id)
    }
    paper = requests.post(url, headers=headers)
    soup = BeautifulSoup(paper.content, 'html.parser')
    return soup


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
        mentioned_uuid = mentioned_uuid.replace('#:uid=', '###')
        mentioned_uuid = mentioned_uuid.replace('#:h2=', '###')
        mentioned_uuid = mentioned_uuid.replace('&h2=', '###')     
        mentioned_uuid = mentioned_uuid.split("###")[1]       
        diventi_title = diventi_universale_soup.select_one('[data-usually-unique-id="{}"]'.format(mentioned_uuid))
        if diventi_title:
            diventi_title = diventi_title.parent
            if diventi_title.h1:
                diventi_title.h1.extract()
            if diventi_title.h2:
                diventi_title.h2.extract()
            while 1:
                diventi_paragraph = diventi_title.next_sibling
                if diventi_paragraph:
                    if diventi_paragraph.h1 or diventi_paragraph.h2:
                        break
                    else:                        
                        diventi_title.append(diventi_paragraph)
                else:
                    break
                #if diventi_next_paragraph is None:
                #    diventi_paragraph = diventi_paragraph.parent
                #else:
                #    diventi_paragraph = diventi_next_paragraph
                #next_title_found = 0
                #for child in diventi_paragraph.children:
                #    if child.h2 or child.h1:
                #        next_title_found = 1    
                #if next_title_found:
                #    break                    
                #diventi_title.append(diventi_paragraph)
            p.parent.parent.replace_with(diventi_title)