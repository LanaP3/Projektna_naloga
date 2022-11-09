from asyncio.log import logger
import csv
import json
import os
import requests
import sys
import logging
import re
from datetime import datetime
import pandas as pd
import time

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
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.info("Webpage doesn't exist!")
    else:
        location = os.path.dirname(file_name)
        if location:
            os.makedirs(location, exist_ok=True)
        with open(file_name, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            logger.info("HTML saved!")
    
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
    not_rated_str = 'Not rated yet'
    
    for block in block_sample.finditer(html):

        # audiobook hasn't been rated yet
        if not_rated_str in block.group(0):
            continue
        audiobook = audiobook_sample.search(block.group(0)).groupdict()
        audiobook['release_date'] = audiobook['release_date'].strip()
        audiobook['author'] = audiobook['author'].replace('"','')

        # add id
        audiobook['audiobook_id'] = audiobook['audiobook_link'][:10] # should have used [-10:]... fixed in the end

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
        
        title = audiobook['title']
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

def check_if_valid(file_path):
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
    return html != ''

def main():
    '''
    Summary
    ----------

    Returns
    ----------
    '''
    audiobooks = []
    audiobooks_2 = []
    for file_name in os.listdir('html_files'):
        logger.info(f'Reading from {file_name}.............')
        html_path = os.path.join('html_files', file_name)
        for audiobook in read_from_html(html_path):

            ## create row for audiobooks.csv
            #audiobooks.append(audiobook)

            # open audiobook link
            title = audiobook['title']
            logger.info(f'Opening page for {title}...')
            url = find_audiobook_url(audiobook['audiobook_link'])
            # try to open the webpage
            request = requests.get(url)
            if request.status_code == 200:
                save_html(url, f'current_audiobook.html')
                # check if valid 
                if check_if_valid('current_audiobook.html'):
                    audiobook_2 = read_from_html_2('current_audiobook.html')
                    audiobooks_2.append(audiobook_2)
                    # add row to audiobooks.csv
                    audiobooks.append(audiobook)
                    os.remove('current_audiobook.html')

                    # logging
                    logger.info(f'Data for {title} is saved!')
                else:
                    logger.info('Something went wrong when downloading webpage html...')

            else:
                logger.info("Audiobook webpage doesn't exist...")

    field_names = ['audiobook_id', 'title', 'author', 'narrator', 'summary', 'audiobook_link', 'length', 'release_date', 'price']
    write_csv(audiobooks, field_names, 'audiobooks.csv')

    field_names_2 = ['audiobook_id', 'categories', 'rating_overall', 'rating_performance', 'rating_story']
    write_csv(audiobooks_2, field_names_2, 'audiobooks_2.csv')


#main()

# when creating audiobook_id column, used [:10] instead of [-10:]
# forgot to write audiobook_id column in audiobooks_2.csv, they are in the same order as in audiobooks.csv, therefore I will just copy the row
# the following function will fix these problems:
def correct_missing_ids():
    df = pd.read_csv(".\\audiobooks.csv")
    df_2 = pd.read_csv(".\\audiobooks_2.csv")
    id_column = df['audiobook_link'].apply(lambda x: x[-10:])
    df['audiobook_id'] = id_column
    df_2['audiobook_id'] = id_column
    # update files
    df.to_csv(".\\audiobooks.csv")
    df_2.to_csv(".\\audiobooks_2.csv")

#correct_missing_ids()