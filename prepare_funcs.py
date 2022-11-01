from asyncio.log import logger
import csv
import json
import os
import requests
import sys
import logging
import re

# logging
LOGGER = logging.getLogger()
logging.basicConfig(
    format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level = logging.INFO)

def prepare_folder(file_name):
    location = os.path.dirname(file_name)
    if location:
        os.makedirs(location, exist_ok=True)

def page_url(n):
    return f'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=review-rank&page={n}&ref=a_search_c4_pageNum_{n}'

def save_website(url, file_name):
    '''
    Summary
    ----------
    Data from a webpage is read and stored.

    Parameters
    ----------
    url (str): url address of a webpage
    file_name (str): name of file in which data will be written

    Returns
    ----------
    nothing
    '''
    
    try:
        logger.info(f'Saving {url}...')
        sys.stdout.flush()
        if os.path.isfile(file_name):
            logger.info('Allready saved!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.info("Webpage doesn't exist!")
    else:
        prepare_folder(file_name)
        with open(file_name, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            logger.info("Saved!")

def read_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        return file.read()
    
def write_csv(dictionaries, field_names, file_name):
    prepare_folder(file_name)
    with open(file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dictionaries)

def write_json(object, file_name):
    prepare_folder(file_name)
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(object, json_file, indent=4, ensure_ascii=False)

def filter_data():
    audiobooks = {}

    #later move to separate json:
    title_start = '''
    <h2  class="bc-heading
    bc-color-base
    
    
    
    
    
    
    bc-text-bold" >
    '''
    title_end = '</h2>'

    author_start = '''
    <li class="bc-list-item" >
    
                        By:
                        
    '''
    author_end = '''
        
                    
</li>
    '''

    length_start = '''
    <li class="bc-list-item" >
    
                        Length: 
    '''
    length_end = '''
    
                    
</li>
    '''

    rating_start = '''
    <span class="bc-text
    bc-pub-offscreen"  >
    '''
    rating_end = '</span>'

    release_date_start = '''
    <span class="bc-text
    
    bc-size-small 
    
    bc-color-secondary"  >Release date:
                                    
    '''
    release_date_end = '''
    
                                  </span>
    '''

    audiobook_link_start = '''
    <h3  class="bc-heading
    bc-color-link
    bc-pub-break-word 
    
    
    
    bc-size-medium" >
                              
                              
                                
                                  <a class="bc-link
    
    
    bc-color-link" tabindex="0"  href="
    '''
    audiobook_link_end = '">'

    price_start = '''
    <span class="bc-text
    
    bc-size-base 
    
    bc-color-base"  >
            
    '''
    price_end = '''
    
        </span>
    '''

    for feature in ['title', 'author', 'length', 'rating', 'release_date', 'audiobook_link', 'price']:
        start = eval(feature+'_start')
        end = eval(feature+'_end')
        feature = []
        feature.append()

    return audiobooks

def read_json(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
        return data

def count_blocks():
    structure_json = read_json(os.path.join(os.getcwd(), "structure.json"))
    href = structure_json['block']['start'] + '.+?' + structure_json['block']['stop']
    html = os.path.join(os.getcwd(), "first_page.html")
    blocks = re.findall(b'href="(http[s]?://.*?)"', html)
    n=0
    for block in blocks:
        n += 1
    print(n)

def collect_audiobooks():
    num_pages = 1
    for page in range(num_pages):
        page_html = page_url(page+1)

#save_website(page_url(1),'first_page.html')

'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=popularity-rank&ref=a_search_c4_pageSize_3'
'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=popularity-rank&page=1&ref=a_search_c4_pageNum_1'
'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=review-rank&ref=a_search_c1_sort_5&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r=HPJRFW8R105V76N03B8W'

'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=popularity-rank&ref=a_search_c4_pageSize_3&      pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=1RY4P34953V6YKGJQR7Y'
'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=popularity-rank&page=2&ref=a_search_c4_pageNum_1&pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=9YWG42D9Z4SNPTYPE2C0'
'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=popularity-rank&page=3&ref=a_search_c4_pageNum_2&pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=QGQ7E6213JXD1DYBTP0V'

count_blocks()