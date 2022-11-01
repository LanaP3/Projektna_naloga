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
    return f'https://www.audible.com/search?feature_six_browse-bin=18685580011&pageSize=50&sort=review-rank&page={n}&ref=a_search_c4_pageNum_{n}'

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

def delete_html(file_name):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''
    os.remove(file_name)

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
    df =  pd.DataFrame(data={'Title':[], 'Author':[], 'Narrator':[], 'Release':[], 'Length':[], 'Cost':[], 'Rating':[], 'Categories':[]})
    for n in range(num_pages):
        url = page_url(n+1)
        save_html(url, 'current_page.html')
        partial_df = create_partial_df('current_page.html')
        delete_html('current_page.html')
        add_to_df(partial_df)
    return df