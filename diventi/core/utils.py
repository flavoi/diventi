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
    tables = paper_soup.find_all('table')
    for table in tables: 
        table['class'] = 'my-2'
        table['style'] = ''
    table_columns = paper_soup.find_all('td')
    for td in table_columns:
        td['style'] = ''    
    return paper_soup


def render_paper_images_by_direct_url(paper_soup):
    """
        Substitutes direct links in tables with the rendered image.
        Image links should be hosted in dropbox and written with "raw=1" parameter.
    """
    links = paper_soup.find_all('a')
    for link_tag in links:
        image_link = link_tag.get('href')
        whitelist_links = [
            '.png?raw=1',
            '.jpg?raw=1',
        ]
        if [link for link in whitelist_links if(link in image_link)]:            
            image_soup = BeautifulSoup('', 'html.parser')
            image_tag = image_soup.new_tag('img')
            image_tag['src'] = 'data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
            image_tag['data-src'] = image_link            
            image_tag['class'] = 'img-fluid rounded mx-auto'
            is_table_link = link_tag.find_parent('table')
            if is_table_link:
                image_tag['class'] = 'rounded mx-auto'
            else:
                image_tag['class'] = 'w-75 d-block p-2 rounded mx-auto'
            link_tag = link_tag.find_parent('span')            
            link_tag.replace_with(image_tag)
    return paper_soup


def render_paper_code_blocks(paper_soup):
    """
        Substitutes code blocks with quick's style alerts.
    """
    codes = paper_soup.find_all('code')
    for code_tag in codes:
        code_content = code_tag.findChildren()
        alert_soup = BeautifulSoup('', 'html.parser')
        alert_tag = alert_soup.new_tag('div')
        alert_tag['role'] = 'alert'
        alert_tag['class'] = 'alert alert-outline-primary my-1'
        for child in code_content:
            alert_tag.append(child)
        code_tag = code_tag.find_parent('div')
        code_tag.replace_with(alert_tag)
    return paper_soup


def remove_dropbox_placeholders(paper_soup):
    """
        Removes dropbox image previews from the document. 
    """
    images = paper_soup.find_all('img')
    blacklist_links = [
        '2753.png',
        '?dl=0',
    ]
    for image_tag in images:
        image_target = image_tag.get('data-src')
        if image_target and [link for link in blacklist_links if(link in image_target)]:
            image_tag.extract()
    links = paper_soup.find_all('a')
    for link_tag in links:        
        link_target = link_tag.get('data-target-href')
        if link_target and [link for link in blacklist_links if(link in link_target)]:
            link_tag.extract()    
    dropbox_galleries = paper_soup.find_all('span', class_='gallery')
    for gallery_tag in dropbox_galleries:
        gallery_tag.extract()
    return paper_soup



