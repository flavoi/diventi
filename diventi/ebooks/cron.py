"""
    This script contains the cron jobs related to the ebooks app.
    We use cron job to schedule background tasks.
"""
import datetime

from django.conf import settings
from django.utils.translation import (
    activate,
    get_language,
    gettext_lazy as _
)

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
    books = Book.objects.all().filter(continuous_update=True)
    for language in settings.LANGUAGES:
        activate(language[0])
        lan = get_language()
        print('Lingua corrente: %s' % lan)
        print(books)
        for book in books:
            if book.paper_id:
                print('Elaboro {}'.format(book.title_it))
                paper_soup = render_dropbox_paper_soup(book.paper_id)
                filepath = settings.BASE_DIR / 'templates/ebooks/partials/book_paper_{}_{}.html'.format(book.id, language[0]) 
                with open(filepath, 'w', encoding='utf-8') as f:
                    print('Stampo %s' % filepath)
                    f.write(str(paper_soup))
            else:
                pass
    return 1