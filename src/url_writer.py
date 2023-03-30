import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv

import logging
import logging.config

def url_writer_script(url):

    load_dotenv()

    """Log Parameters

    """
    logging.config.fileConfig('../config/logging.conf')

    """Base Parameters
    
    Base connection parameters
    """
    URL=url
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    }

    response = requests.get(URL,HEADERS)
    soup = BeautifulSoup(response.content,'html.parser')

    """File creation

    S3 bucket connection and file uploading    
    """
    with open('/home/icharo-tb/workspace/GW2-SRS_AWS-Docker/src/tmp/urls.txt','a') as fh:

        for link in soup.find_all('a'):
            url_str = 'https://gw2wingman.nevermindcreations.de'
            data = link.get('href')
            
            try:
                log_str = url_str+data
                if log_str.endswith('apikey'):
                    log_str.replace('apikey','\n')
                elif log_str.endswith('void(0)'):
                    log_str.replace('void(0)','\n')
                else:
                    fh.write(log_str)
                    fh.write('\n')
            except Exception as e:
                logging.warning(e)