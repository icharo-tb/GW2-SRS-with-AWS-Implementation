from url_writer import url_writer_script
from s3_load import s3_loader
from s3_read import s3_reader

from main_etl import gw2_etl

import logging
import logging.config

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

    cnt = 0

    while cnt <= 18:
        try:
            url = f'https://gw2wingman.nevermindcreations.de/content/raid/{boss_list[cnt]}?onlyCM=onlyNM'
            logging.info(url)
            url_writer_script(url)
        except Exception as e:
            logging.warning(e)
        finally:
            cnt += 1
            cnt % len(boss_list)

    try:
        s3_loader()
    except Exception as e:
        logging.warning(e)

    url_list = s3_reader('gw2-srs-bucket','urls.txt')

    for url in url_list:
        gw2_etl(url)