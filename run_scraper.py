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
    scraper = Scraper()
    scraper.run()
    mongo_operator = MongoOperator()
    mongo_operator.add_record(scraper.dataset)


if __name__ == '__main__':
    main()
