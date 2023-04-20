from url_writer import url_writer_script
from s3_load import s3_loader
from s3_read import s3_reader

from main_etl import gw2_etl

import logging
import logging.config

import os

"""Logger conf
"""
logging.config.fileConfig("../config/logging.conf")

"""Boss Tag Rotator
"""

boss_list = [
    'vg','gors','sab','sloth','matt','kc','xera',
    'cairn','mo','sam','dei','sh','dhuum','ca',
    'twins','q1','adina','sabir','q2'
    ]

if __name__=='__main__':

    def etl_executer(rot:list):

        cnt = 0

        while cnt <= 18:
            try:
                url = f'https://gw2wingman.nevermindcreations.de/content/raid/{rot[cnt]}?onlyCM=onlyNM'
                logging.info(url)
                url_writer_script(url)
            except Exception as e:
                logging.warning(e)
            finally:
                cnt += 1
                cnt % len(rot)

        try:
            s3_loader('./tmp/urls.txt','gw2-srs-bucket','urls.txt')
            logging.info('File loaded to S3.')
        except Exception as e:
            logging.warning(e)

        url_list = s3_reader('gw2-srs-bucket','urls.txt')

        cnt = 0

        for url in url_list:

            cnt += 1

            try:
                st_url = url.strip()
                rep = st_url.replace('log', 'logContent')
                logging.info(rep)
                gw2_etl(rep)
                logging.info(f'Log nº: {cnt}')
            except IndexError as e:
                logging.warning(e)
                continue

        os.remove('./tmp/*')

    
    etl_executer(rot=boss_list)