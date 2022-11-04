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
    
def nekineki(file_name):
    with open(file_name, encoding='utf-8') as f:
        html =  f.read()
    
    block_sample = re.compile(
        r'productListItem\" aria-label=.*?'
        r'Free with 30-day trial',
        flags=re.DOTALL
    )
    #audiobook_sample = re.compile(
    #    r"productListItem\" aria-label='(?P<title>.*?)'>"
    #    r'bc-size-medium\" >\s*<a class=\"bc-link\s*bc-color-link\" tabindex=\"0\"  href=\"(?P<audiobook_link>.*?)\">'
    #    r'Release date:(?P<releade_date>.*?)</span>'
    #    r'bc-color-base\"  >Regular price: </span>\s*<span class=\"bc-text\s*bc-size-base \s*bc-color-base\"  >\s*(?P<price>.*?)\s',
    #    flags=re.DOTALL
    #)
    title_sample = re.compile(
        r"productListItem\" aria-label='(?P<title>.*?)'>", 
        flags=re.DOTALL
    )
    audiobook_link_sample = re.compile(
        r'bc-size-medium\" >\s*<a class=\"bc-link\s*bc-color-link\" tabindex=\"0\"  href=\"(?P<audiobook_link>.*?)\">', 
        flags=re.DOTALL
    )
    release_date_sample = re.compile(
        r'Release date:(?P<releade_date>.*?)</span>', 
        flags=re.DOTALL
    )
    price_sample = re.compile(
        r'bc-color-base\"  >Regular price: </span>\s*<span class=\"bc-text\s*bc-size-base \s*bc-color-base\"  >\s*(?P<price>.*?)\s', 
        flags=re.DOTALL
    )
    length_sample = re.compile(
        r'Length:(?P<length>.*?)</span>', #2times per audiobook
        flags=re.DOTALL
    )

    for block in block_sample.finditer(html):
        #audiobook = audiobook_sample.search(block.group(0)).groupdict()
        title = title_sample.search(block.group(0))
        audiobook_link = audiobook_link_sample.search(block.group(0))
        release_date = release_date_sample.search(block.group(0))
        price = price_sample.search(block.group(0))
        length = length_sample.search(block.group(0))
        #print([length, title, audiobook_link, release_date, price])
        print(audiobook_link)

#nekineki('html_files/first_page.html')
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
    num_pages = 20
    df =  pd.DataFrame(data={'Title':[], 'Author':[], 'Narrator':[], 'Release':[], 'Length':[], 'Price':[], 'Rating':[], 'Categories':[]})
    for html_file in os.listdir('html_files'):
        html_filename = '...'
        partial_df = create_partial_df(html_filename)
        add_to_df(partial_df)
    return df

save_all_html()