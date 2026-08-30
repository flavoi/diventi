from django.conf import settings

from diventi.products.models import Product
from diventi.products.utils import get_product_context
from diventi.blog.models import Article
from diventi.feedbacks.models import Survey
from diventi.packages.models import Package


# Get the relevant data for a selected landing page
def get_landing_context(request, page):
    if page is None:
        raise Http404(_('This page is not available yet.'))
    sections = page.sections.all().prefetch()
    featured_section = sections.featured()
    pinned_products = Product.objects.pinned_list().prefetch()
    pinned_articles = Article.objects.pinned_list().prefetch()
    if featured_section:
        pass
    elif sections.exists():
        featured_section = sections.first()        
    else:
        raise Http404(_('This page is not available yet.'))
    sections = sections.exclude(id=featured_section.id)    
    context = {
        'landing_page': page,
        'sections': sections,
        'featured_section': featured_section,
        'pinned_products': pinned_products,
        'pinned_articles': pinned_articles,
    }
    return context