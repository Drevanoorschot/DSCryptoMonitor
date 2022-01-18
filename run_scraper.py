import logging
import sys

import django
from django.conf import settings

from scraper.mongo import MongoOperator

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=['coins']
)
django.setup()
from scraper.scraper import Scraper


def main():
    logger = logging.getLogger()
    file_handler = logging.FileHandler(filename='scraper.log', mode='w')
    out_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    out_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(out_handler)
    logger.setLevel(logging.INFO)

    scraper = Scraper()
    scraper.run()
    mongo_operator = MongoOperator()
    mongo_operator.add_record(scraper.dataset)


if __name__ == '__main__':
    main()
