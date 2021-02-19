import requests
from bs4 import BeautifulSoup

from django.conf import settings
from django.utils.translation import gettext as _


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


def render_paper_tables(paper_soup):
    """
        Adds vertical spacing to tables and encapsulates
        them in a collasping card.
    """
    tables = paper_soup.find_all('table')
    collapse_counter = 1
    for table in tables:
        table['style'] = ''

        collapse_soup = BeautifulSoup('', 'html.parser')
        
        collapse_l1_tag = table.wrap(collapse_soup.new_tag("div", **{"class": "card-body"}))
        collapse_l2_tag = collapse_l1_tag.wrap(collapse_soup.new_tag("div"))       
        collapse_l2_tag['id'] = 'collapse-{}'.format(collapse_counter)
        collapse_l2_tag['aria-labelledby'] = 'heading-{}'.format(collapse_counter)
        collapse_l2_tag['data-parent'] = '#accordion-{}'.format(collapse_counter)
        collapse_l2_tag['class'] = "collapse"
       
        collapse_title_l1_tag = collapse_soup.new_tag("h6")
        collapse_title_l1_tag['class'] = 'mb-0'
        collapse_title_l1_tag.string = _('Discover')
        collapse_l2_tag = collapse_l2_tag.insert_before(collapse_title_l1_tag)

        collapse_title_l2_tag = collapse_title_l1_tag.wrap(collapse_soup.new_tag("div"))
        collapse_title_l2_tag['class'] = 'card-header py-4'
        collapse_title_l2_tag['id'] = 'heading-{}'.format(collapse_counter)
        collapse_title_l2_tag['data-toggle'] = 'collapse'
        collapse_title_l2_tag['role'] = 'button'
        collapse_title_l2_tag['data-target'] = '#collapse-{}'.format(collapse_counter)
        collapse_title_l2_tag['aria-expanded'] = 'false'
        collapse_title_l2_tag['aria-controls'] = 'collapse-{}'.format(collapse_counter)      
      
        collapse_wrapper_tag = collapse_title_l2_tag.find_parent('div')
        collapse_wrapper_tag['class'] = 'card'
        collapse_wrapper_tag['style'] = ''

        collapse_wrapper_tag = collapse_wrapper_tag.find_parent('div')
        collapse_wrapper_tag.name = 'div'
        collapse_wrapper_tag['id'] = 'accordion-{}'.format(collapse_counter)
        collapse_wrapper_tag['class'] = 'accordion mt-2 mb-4'       

        collapse_counter += 1
    table_columns = paper_soup.find_all('td')
    for td in table_columns:
        td['style'] = ''    
    return paper_soup


def render_paper_hr(paper_soup):
    """
        Adjust horizontal lines' visual style.
    """
    lines = paper_soup.find_all('hr')
    for line_tag in lines:
        line_tag['style'] = ''
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
            is_table_link = link_tag.find_parent('table')
            if is_table_link:
                image_tag['class'] = 'rounded mx-auto'
            else:
                image_tag['class'] = 'img-fluid rounded shadow-lg'
                figure_tag = image_soup.new_tag('figure')
                figure_tag['class'] = 'figure'
                figure_tag.append(image_tag)
                image_tag = figure_tag
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
        alert_tag['class'] = 'alert bg-translucent-secondary my-0 py-1'
        for child in code_content:
            if child.string:
                alert_tag.append(child.string)
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
        if mentioned_uuid: # Dropbox meta 2020
            diventi_title = extract_diventi_content(mentioned_uuid, diventi_universale_soup)
            if diventi_title:
                p.parent.parent.replace_with(diventi_title)
        elif mentioned_href: # Dropbox meta 2021
            diventi_title = extract_diventi_content(mentioned_href, diventi_universale_soup)
            if diventi_title:
                p.parent.parent.parent.replace_with(diventi_title)