import requests, base64, json
from bs4 import BeautifulSoup

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.text import slugify


def get_dropbox_paper_soup(paper_id, oauth=1):
    """
        Connects to dropbox API and export the Paper's content into memory
    """
    url = "https://content.dropboxapi.com/2/files/export"
    if oauth:
        headers = {
            "Authorization": "Bearer {}".format(settings.DROPBOX_ACCESS_TOKEN),
            "Dropbox-API-Arg": "{\"path\":\"%s\",\"export_format\":\"html\"}" % paper_id,
        }
    else:
        refresh_url = "https://api.dropbox.com/oauth2/token"
        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': settings.DROPBOX_REFRESH_TOKEN,
            'client_id': settings.DROPBOX_APP_KEY,
            'client_secret': settings.DROPBOX_APP_SECRET,
        }
        r = requests.post(refresh_url, data=refresh_data)
        access_tokenn = r.json().get('access_token')
        headers = {
            "Authorization": "Bearer {}".format(access_tokenn),
            "Dropbox-API-Arg": "{\"path\":\"%s\",\"export_format\":\"html\"}" % paper_id,
        }
    r = requests.post(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_paper_filename(paper_id, paper_lan):
    return 'ebooks/partials/book_paper_{}_{}.html'.format(paper_id, paper_lan)

def parse_paper_soup(paper_filename):
    """
        Load soup from html file.
    """
    for template_dir in settings.TEMPLATES[0]['DIRS']:
        with open(template_dir / paper_filename, 'r', encoding='utf-8') as paper_file:
            soup = BeautifulSoup(paper_file, 'html.parser')
            return soup
    return 0


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
        Inject tables with the correct visual styles depending
        on the table's nature.
    """
    tables = paper_soup.find_all('table')
    table_counter = 1
    for table in tables:
        if table.get('class') and table.get('class')[0] == 'table-top-header':
            table = render_sortable_table(table, table_counter)           
        else:
            table = render_card_table(table, table_counter)         
        table_counter += 1 
    return paper_soup    


def render_sortable_table(table, table_counter):
    """
        Prepare tables of jQuery datatables plugin.
    """
    table['class'] = 'display compact sortable w-100'
    table['id'] = 'tabella-{}'.format(table_counter)
    table['style'] = ''
    table_columns = table.find_all('td')
    for td in table_columns:
        td['style'] = ''
    return table


def render_card_table(table, collapse_counter):
    """
        Adds vertical spacing to tables and encapsulates
        them in a collasping card.
    """
   
    table['style'] = ''
    table['class'] = 'clear-user-agent-styles cards'

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

    table_columns = table.find_all('td')
  
    return table


def render_paper_hr(paper_soup):
    """
        Adjust horizontal lines' visual style.
    """
    lines = paper_soup.find_all('hr')
    for line_tag in lines:
        line_tag['style'] = ''
        line_tag['class'] = 'my-3'
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
                image_tag['class'] = 'rounded'
                image_tag['style'] = 'width: 255px;'
            else:
                image_tag['class'] = 'img-fluid rounded hover-translate-y-n3 hover-shadow-lg'
                figure_tag = image_soup.new_tag('figure')
                figure_tag['class'] = 'figure my-1'
                figure_tag.append(image_tag)
                image_tag = figure_tag
            link_tag = link_tag.find_parent('span')            
            link_tag.replace_with(image_tag)
    return paper_soup


def render_paper_images(paper_soup):
    """
        Renders paper uploaded images with default visual styles.
    """
    images = paper_soup.find_all('img')
    for image_tag in images:
        image_tag['style'] = ''
        image_tag['class'] = 'img-fluid my-3 hover-translate-y-n3 hover-shadow-lg'
    return paper_soup


def render_paper_fancy_images(paper_soup):
    """
        Renders paper uploaded images with a fancy box.
    """
    images = paper_soup.find_all('img')
    for image_tag in images:
        image_tag['style'] = 'fancy'
        image_tag['class'] = 'img-fluid my-3 hover-translate-y-n3 hover-shadow-lg'
        fancy_soup = BeautifulSoup('', 'html.parser')
        fancy_tag = fancy_soup.new_tag('a')
        fancy_tag['data-fancybox'] = ''
        fancy_tag['href'] = image_tag.get('src')
        fancy_tag['data-caption'] = image_tag.get('alt')
        image_tag = image_tag.wrap(fancy_tag)
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


def render_paper_headings(paper_soup):
    """
        Remove dropbox paper styles from the headings and adjust
        the visual style to improve readability as much as possibile.
        It defers table formatting to the appropriate module.
    """
    h2_title_id = ''
    for title in paper_soup.find_all('h2'):
        title['style'] = ''
        title['id'] = title['data-usually-unique-id']
        h2_title_id = title['id']
        title['class'] = 'h4 mt-4 mb-1 text-primary'

    first_title = 1
    for title in paper_soup.find_all('h1'):
        title['style'] = ''
        title['id'] = title['data-usually-unique-id']
        if first_title:
            title['class'] = 'h2 mt-0 mb-4'
            first_title = 0
        else:
            title['class'] = 'h2 mt-5 mb-4'

    for title in paper_soup.find_all(class_='ace-all-bold-hthree'):
        if not title.find_parents("table"):
            title_soup = BeautifulSoup('', 'html.parser')
            title_tag = title_soup.new_tag('h4')
            title_tag['class'] = 'h5 mt-2 mb-1 text-dark'
            title_tag['id'] = h2_title_id + '-' + slugify(title.text)
            title_tag.string = title.text
            title.replace_with(title_tag)
    paper_soup.select_one('.ace-line').extract()
    return paper_soup


def make_paper_toc_cards(paper_soup):
    """
        Extracts H1 and H2 elements from the page and writes 
        a list of cards with their relative subheadings.
    """
    toc = []
    title_dict = {}
    for title in paper_soup.find_all(['h1', 'h2', 'h4']):
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
        elif title.name == 'h2':
            # Sub-headings nested into headings
            title_dict[parent_title_key].append(
                {
                    'string': title.span.string,
                    'anchor': title['id'],
                    'name': title.name,
                } 
            )
        elif title.name == 'h4' and title.get('id'):
            # Section-headings nested into sub-headings
            title_dict[parent_title_key].append(
                {
                    'string': title.string,
                    'anchor': title['id'],
                    'name': title.name,
                    'class': 'ml-4'
                } 
            )
        else:
            pass
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


def render_dropbox_paper_soup(book_paper_id, oauth=1):
    """
        Invoke all the necessary module to completely render a book page.
    """
    paper_soup = get_dropbox_paper_soup(book_paper_id, oauth)
    diventi_universale_soup = get_dropbox_paper_soup(settings.DIVENTI_UNIVERSALE_PAPER_ID, oauth=0)
    render_diventi_snippets(paper_soup, diventi_universale_soup)
    render_paper_tables(paper_soup)
    render_paper_fancy_images(paper_soup)
    render_paper_code_blocks(paper_soup)
    render_paper_hr(paper_soup)
    render_paper_headings(paper_soup)
    return paper_soup