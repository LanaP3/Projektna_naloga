from asyncio.log import logger
import csv
import json
import os
import requests
import sys
import logging
import re
from datetime import datetime
from datetime import date
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

def find_audiobook_url(audiobook_link):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    ''' 
    return 'https://www.audible.com'+audiobook_link

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
            logger.info('Already saved!')
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
    '''
    Summary
    ----------

    Parameters
    ----------

    Yields
    ----------
    '''
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
        r'bc-size-medium\" >\s*<a class=\"bc-link\s*bc-color-link\" tabindex=\"0\"  href=\"(?P<audiobook_link>.*?)\">.*?'
        r'Length:(?P<length>.*?)</span>.*?'
        r'Release date:(?P<release_date>.*?)</span>.*?',
        flags=re.DOTALL
    )
    summary_sample = re.compile(
        r'<p  class=\"bc-text\s*bc-spacing-small\s*bc-spacing-top-none\s*bc-size-small\s*bc-color-base\">\s*<p>(?P<summary>.*?)</p>',
        flags=re.DOTALL
    )
    narrator_sample = re.compile(
        r'<li class=\"bc-list-item\" >\s*Narrated by:\s*(?P<narrator>.*?)\s*</li>',
        flags=re.DOTALL
    )
    price_sample = re.compile(
        r'bc-color-base\"  >Regular price: </span>\s*<span class=\"bc-text\s*bc-size-base \s*bc-color-base\"  >\s*(?P<price>.*?)\s',
        flags=re.DOTALL
    )
    alternative_price_sample = re.compile(
        r'Regular price: </span>\s*<span class=\"bc-text\s*bc-size-small\s*bc-color-secondary\s*bc-text-strike\"  >\s*(?P<price>.*?)</span>',
        flags=re.DOTALL
    )
    
    for block in block_sample.finditer(html):
        audiobook = audiobook_sample.search(block.group(0)).groupdict()
        audiobook['release_date'] = audiobook['release_date'].strip()
        audiobook['author'] = audiobook['author'].replace('"','')

        # add id
        audiobook['audiobook_id'] = audiobook['audiobook_link'][:10]

        # add summary
        summary = summary_sample.search(block.group(0))
        if summary:
            audiobook['summary'] = str(summary['summary'])
            audiobook['summary'] = audiobook['summary'].replace('<i>','').replace('</i>','').replace('"','').strip()
        if not summary:
            audiobook['summary'] = None
        
        # add price
        price = price_sample.search(block.group(0))
        alternative_price = alternative_price_sample.search(block.group(0))
        if price:
            audiobook['price'] = str(price['price'])
        if alternative_price:
            audiobook['price'] = str(alternative_price['price'])
        
        ## check if narrator, skip audiobook if not (not yet released)
        title = audiobook['title']
        #narrator = narrator_sample.search(block.group(0))
        #if narrator:
        #    
        #    audiobook['narrator'] = str(narrator['narrator']).replace('"','')
        #    yield(audiobook)
        #    logger.info(f'{title} saved!')
        
        # check if already released
        release_date_str = audiobook['release_date']
        release_date = datetime.strptime(release_date_str, '%m-%d-%y')
        today = datetime.today()

        if not release_date > today:
            # add narrator
            narrator = narrator_sample.search(block.group(0))
            audiobook['narrator'] = str(narrator['narrator']).replace('"','')
            
            yield(audiobook)
            logger.info(f'{title} saved!')

        # logging
        else:
            logger.info(f'{title} is not yet released!')
        
def save_all_html():
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''
    for n in range(24):
        page_url = find_page_url(n+1)
        save_html(page_url, f'page_{n+1}.html')

def main():
    '''
    Summary
    ----------

    Returns
    ----------
    '''
    audiobooks = []
    for file_name in os.listdir('html_files'):
        logger.info(f'Reading from {file_name}.............')
        html_path = os.path.join('html_files', file_name)
        for audiobook in read_from_html(html_path):
            audiobooks.append(audiobook)
    field_names = ['audiobook_id', 'title', 'author', 'narrator', 'summary', 'audiobook_link', 'length', 'release_date', 'price']
    write_csv(audiobooks, field_names, 'audiobooks.csv')

def read_from_html_2(file_path):
    '''
    Summary
    ----------

    Parameters
    ----------

    Returns
    ----------
    '''
    with open(file_path, encoding='utf-8') as f:
        html =  f.read()

    categories_sample = re.compile(
        r'digitalData.page.category.primaryCategory = "(?P<categories>.*?)";',
        flags=re.DOTALL
    )
    ratings_sample = re.compile(
        r'>\s*(?P<rating_overall>[.0-9]*?) out of 5\.0.*?'
        r'>\s*(?P<rating_performance>[.0-9]*?) out of 5\.0.*?'
        r'>\s*(?P<rating_story>[.0-9]*?) out of 5\.0',
        flags=re.DOTALL
    )

    audiobook = ratings_sample.search(html).groupdict()
    for rating in audiobook.keys():
        audiobook[rating] = audiobook[rating].strip()
    categories = categories_sample.search(html)
    audiobook['categories'] = categories['categories']
    return audiobook

def main_2(file_path):
    '''
    Summary
    ----------
    - Read csv file
    - Open web page for each audiobook
    - Download html
    - Collect ratings and categories
    - Delete html
    - Save to a new csv file

    Parameters
    ----------
    file_path(str): path to the csv file with audiobooks data
    '''
    audiobooks = []
    df = pd.read_csv(file_path)
    for i, row in df.iterrows():
        url = find_audiobook_url(row['audiobook_link'])
        logger.info(f'Opening {url}...')
        save_html(url, f'current_audiobook.html')
        audiobook = read_from_html_2('current_audiobook.html')
        audiobooks.append(audiobook)
        # logging
        title = row['title']
        logger.info(f'Data for {title} is saved!')
        os.remove('current_audiobook.html')
    field_names = ['audiobook_id', 'categories', 'rating_overall', 'rating_performance', 'rating_story']
    write_csv(audiobooks, field_names, 'audiobooks.csv')

    
    


#read_from_html('html_files/page_10.html')
#save_all_html()
#main()
#print(read_from_html_2('current_audiobook.html'))
main_2('audiobooks.csv')