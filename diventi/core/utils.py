import requests

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


def extract_diventi_content(mention_link, diventi_universale_soup):
    """
        Extract the paragraph between two titles in Diventi Universale.
        It connects via direct link to the desired title.
    """
    mentioned_uuid = mention_link.replace('#:uid=', '###')
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
        return diventi_title
    else:
        return ''


def adjust_paper_visual_styles(paper_soup):
    paper_soup = paper_soup.select('table')
    for table in paper_soup:
        table['class'] = 'my-2'

