""" Diventi URL Configuration """

from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'jsi18n/', JavaScriptCatalog.as_view(domain="django"), name='javascript-catalog'),
    url(r'^comments/default/', include('django_comments.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^\.well-known/', include('letsencrypt.urls')),
    url(r'^reviews/', include('reviews.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('diventi.landing.urls', namespace='landing')),
    path(_('control-panel/'), admin.site.urls),
    path(_('accounts/'), include('diventi.accounts.urls', namespace='accounts')),
    path(_('blog/'), include('diventi.blog.urls', namespace='blog')),
    path(_('applications/'), include('diventi.products.urls', namespace='products')),
    path(_('comments/'), include('diventi.comments.urls', namespace='comments')),
    path(_('feedbacks/'), include('diventi.feedbacks.urls', namespace='feedbacks')),
    path(_('ebooks/'), include('diventi.ebooks.urls', namespace='ebooks')),
    path(_('sheets/'), include('diventi.sheets.urls', namespace='sheets')),
    path(_('payments/'), include('diventi.payments.urls', namespace='payments')),
)