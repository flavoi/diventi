""" Diventi URL Configuration """

from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.i18n import JavaScriptCatalog

from machina import urls as machina_urls

admin.autodiscover()

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(domain="django"), name='javascript-catalog'),
    path('comments/default/', include('django_comments.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reviews/', include('reviews.urls')),
    path('.well-known/', include('letsencrypt.urls')),
    path('.well-known/', include('diventi.brave.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('apps/', include('diventi.products.urls', namespace='products')),
]

urlpatterns += i18n_patterns(
    path('', include('diventi.landing.urls', namespace='landing')),    
    path(_('control-panel/'), admin.site.urls),
    path(_('accounts/'), include('diventi.accounts.urls', namespace='accounts')),
    path(_('blog/'), include('diventi.blog.urls', namespace='blog')),    
    path(_('comments/'), include('diventi.comments.urls', namespace='comments')),
    path(_('feedbacks/'), include('diventi.feedbacks.urls', namespace='feedbacks')),
    path(_('ebooks/'), include('diventi.ebooks.urls', namespace='ebooks')),
    path(_('adventures/'), include('diventi.adventures.urls', namespace='adventures')),
    path(_('community/'), include(machina_urls)),
)