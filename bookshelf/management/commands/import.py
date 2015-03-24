from django.core.management.base import BaseCommand, CommandError

from bookshelf.models import Book, Reading, Entry

import json

class Command(BaseCommand):
    args = '<json file>'
    help = 'Imports a Bookkeeper JSON export file'

    def handle(self, *args, **options):
        filename = args[0]
        print(filename)

        try:
            with open(filename, 'r') as f:
                data = f.read()

            data = json.loads(data)

            # Now load in each book
            for item in data:
                book = Book()
                book.title = item['title']
                book.save()
                
                reading = Reading()
                reading.book = book
                reading.started_date = item['startDate']
                reading.end_page = item['totalPages']

                if item['endDate'] != '0000-00-00' or item['percentage'] == 100:
                    if item['endDate'] != '0000-00-00':
                        reading.finished_date = item['endDate']
                    else:
                        reading.finished_date = item['entries'][-1]['entryDate']
                    reading.status = 'finished'

                if item['hidden'] == True:
                    reading.status = 'abandoned'
                    reading.finished_date = None

                reading.save()

                for e in item['entries']:
                    entry = Entry()
                    entry.reading = reading
                    entry.page_number = e['pageNumber']
                    entry.date = e['entryDate']
                    entry.save()

        except Exception as e:
            print(e)
