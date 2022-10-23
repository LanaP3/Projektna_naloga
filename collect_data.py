from asyncio.log import logger
import csv
import json
import os
import requests
import sys
import logging

# logging
LOGGER = logging.getLogger("wf-monitor")
logging.basicConfig(
    format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level = logging.INFO)

def prepare_folder(file_name):
    location = os.path.dirname(file_name)
    if location:
        os.makedirs(location, exist_ok=True)

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
        prepare_folder()
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
