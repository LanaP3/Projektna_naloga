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

def page_url(n):
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
    
def nekineki():
    re.compile(
        r"productListItem\" aria-label='(?P<title>.*?)'>"
        r'bc-size-medium\" >\s*<a class=\"bc-link\s*bc-color-link\" tabindex=\"0\"  href=\"(?P<audiobook_link>.*?)\">'
        r'Length:(?P<length>.*?)</span>' #2times per audiobook
        r'Release date:(?P<releade_date>.*?)</span>'
        r'bc-color-base\"  >Regular price: </span>\s*<span class=\"bc-text\s*bc-size-base \s*bc-color-base\"  >\s*(?P<price>.*?)\s'
               )

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
    for n in range(num_pages):
        url = page_url(n+1)
        save_html(url, f'page_{n+1}.html')
    for html_file in os.listdir('html_files'):
        html_filename = '...'
        partial_df = create_partial_df(html_filename)
        add_to_df(partial_df)
    return df