from asyncio.log import logger
import csv
import json
import os
import requests
import sys
import logging
import re
import pandas as pd

# logging
LOGGER = logging.getLogger()
logging.basicConfig(
    format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level = logging.INFO)

def find_page_url(n):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    ''' 
    return f'https://www.audible.com/search?node=18685580011&pageSize=50&sort=popularity-rank&page={n}&ref=a_search_c4_pageNum_{n-1}'

def save_html(url, file_name):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
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
        location = os.path.dirname(file_name)
        if location:
            os.makedirs(location, exist_ok=True)
        with open(file_name, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            logger.info("Saved!")

def create_partial_df(file_name):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''

def add_to_df(partial_df):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''
    
def write_csv(dictionaries, field_names, file_name):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''
    location = os.path.dirname(file_name)
    if location:
        os.makedirs(location, exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dictionaries)

def read_from_html(file_path):
    with open(file_path, encoding='utf-8') as f:
        html =  f.read()
    
    block_sample = re.compile(
        r'productListItem\" aria-label=.*?'
        r'Free with 30-day trial',
        flags=re.DOTALL
    )
    audiobook_sample = re.compile(
        r"productListItem\" aria-label='(?P<title>.*?)'>.*?"
        r'<li class=\"bc-list-item\" >\s*By:\s*(?P<author>.*?)\s*</li>.*?'
        r'<li class=\"bc-list-item\" >\s*Narrated by:\s*(?P<narrator>.*?)\s*</li>.*?'
        r'<p  class=\"bc-text\s*bc-spacing-small\s*bc-spacing-top-none\s*bc-size-small\s*bc-color-base\">\s*<p>(?P<summary>.*?)</p>.*?'
        r'bc-size-medium\" >\s*<a class=\"bc-link\s*bc-color-link\" tabindex=\"0\"  href=\"(?P<audiobook_link>.*?)\">.*?'
        r'Length:(?P<length>.*?)</span>.*?'
        r'Release date:(?P<release_date>.*?)</span>.*?'
        r'bc-color-base\"  >Regular price: </span>\s*<span class=\"bc-text\s*bc-size-base \s*bc-color-base\"  >\s*(?P<price>.*?)\s',
        flags=re.DOTALL
    )

    for block in block_sample.finditer(html):
        audiobook = audiobook_sample.search(block.group(0)).groupdict()
        audiobook['summary'] = audiobook['summary'].replace('<i>','').replace('</i>','').strip()
        audiobook['release_date'] = audiobook['release_date'].strip()
        yield audiobook

def save_all_html():
    for n in range(24):
        page_url = find_page_url(n+1)
        save_html(page_url, f'page_{n+1}.html')

def main():
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''
    #df =  pd.DataFrame(data={'Title':[], 'Author':[], 'Narrator':[], 'Release':[], 'Length':[], 'Price':[], 'Rating':[], 'Categories':[]})
    audiobooks = []
    for file_name in os.listdir('html_files'):
        html_path = os.path.join('html_files', file_name)
        for audiobook in read_from_html(html_path):
            audiobooks.append(audiobook)
    field_names = ['title', 'author', 'narrator', 'summary', 'audiobook_link', 'length', 'release_date', 'price']
    write_csv(audiobooks, field_names, 'audiobooks.csv')
#read_from_html('html_files/page_2.html')
#save_all_html()
main()