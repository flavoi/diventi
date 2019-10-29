import stripe

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from cuser.middleware import CuserMiddleware

from diventi.products.models import Product 
from diventi.products.views import AddToUserCollectionView

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomePageView(TemplateView):
    template_name = 'payments/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['product'] = Product.objects.all().first()
        return context


def charge(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=5,
                currency='eur',
                description='A Diventi charge',
                source=request.POST['stripeToken'],
            )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print('Status is: %s' % e.http_status)
            print('Type is: %s' % e.error.type)
            print('Code is: %s' % e.error.code)
            # param is '' in this case
            print('Param is: %s' % e.error.param)
            print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            pass
        user = CuserMiddleware.get_user()
        product.buyers.add(user)
        messages.success(request, _('You paid {} {} for {}'.format('eur', 5, product.title)))
        return redirect(product)