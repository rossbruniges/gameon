import datetime
import hashlib
import os
import csv
import codecs
import cStringIO

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings


def _upload_path(tag):
    def _upload_path_tagged(instance, filename):
        now = datetime.datetime.now()
        path = os.path.join(now.strftime('%Y'), now.strftime('%m'),
                            now.strftime('%d'))
        hashed_filename = (hashlib.md5(filename +
                           str(now.microsecond)).hexdigest())
        __, extension = os.path.splitext(filename)
        return os.path.join(tag, path, hashed_filename + extension)
    return _upload_path_tagged


def get_page(data):
    """Determines the page number"""
    try:
        page = int(data.get('page', '1'))
    except (ValueError, TypeError):
        page = 1
    return page


def get_paginator(queryset, page_number, items=settings.PAGINATOR_SIZE):
    """"Generates a paginator object with the size and page provided"""
    paginator = Paginator(queryset, items)
    try:
        paginated_query = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        paginated_query = paginator.page(paginator.num_pages)
    return paginated_query


# In case we get unicode in the DB we use a custom reader able to handle it
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
