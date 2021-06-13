"""
    This script contains the cron jobs related to the ebooks app.
    We use cron job to schedule background tasks.
"""
import datetime

from django.conf import settings
from django.utils.translation import get_language

from .models import Book

from .utils import (
    render_dropbox_paper_soup
)


def fetch_paper_books():
    """
        Fetches paper contents from every book and stores them in a html file.
    """
    ct = datetime.datetime.now()
    print('Ultima stampa di paper: %s' % ct)
    books = Book.objects.all()
    for book in books:
        if book.paper_id:
            print('Elaboro %s' % book.title_it)
            lan = get_language()
            print('Lingua corrente: %s' % lan)
            paper_soup = render_dropbox_paper_soup(book.paper_id)
            filepath = settings.BASE_DIR / 'templates/ebooks/partials/book_paper_{}.html'.format(book.id) 
            with open(filepath, 'w') as f:
                print('Stampo %s' % filepath)
                f.write(str(paper_soup))
        else:
            pass
    return 1