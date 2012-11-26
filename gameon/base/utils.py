import datetime
import hashlib
import os

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
