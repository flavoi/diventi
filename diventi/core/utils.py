import requests

from bs4 import BeautifulSoup, Tag

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
    """
        Adds vertical spacing to tables.
    """
    paper_soup = paper_soup.select('table')
    for table in paper_soup: 
        table['class'] = 'my-2'
    return paper_soup


def adjust_paper_image_styles(paper_soup):
    """
        Adds center position and deferred loading to images.
        In addition, it removes complex gallery tags with bootstrap styled images.
    """
    paper_soup = paper_soup.select('img')
    for image in paper_soup: 
        image_link = image.get('src')
        if image_link:
            image['src'] = 'data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
            image['data-src'] = image_link   
        big_tag = image.find_parent('span', class_='gallery')        
        if image.find_parent('table') and not image.get('data-emoji-ch'):
            image['class'] = 'img-fluid rounded mx-auto'
            big_tag.replace_with(image)
        elif big_tag:
            image['class'] = 'w-50 p-1 mx-auto d-block img-fluid rounded'
            big_tag.replace_with(image)
    return paper_soup


def render_paper_images_by_direct_url(paper_soup):
    """
        Substitutes direct links in tables with the rendered image.
        Image links should be hosted in dropbox and written with "raw=1" parameter.
    """
    paper_soup = paper_soup.select('table')
    for table in paper_soup:
        links = table.find_all('a')
        for link_tag in links:
            image_link = link_tag.get('href')
            if '.png?raw=1' in image_link:
                link_tag = link_tag.find_parent('span', class_='url')
                image_soup = BeautifulSoup('', 'html.parser')
                image_tag = image_soup.new_tag('img')
                image_tag['src'] = 'data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
                image_tag['data-src'] = image_link
                image_tag['class'] = 'img-fluid rounded mx-auto'
                link_tag.replace_with(image_tag)
    return paper_soup




