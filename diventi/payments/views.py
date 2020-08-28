import stripe, json

from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail

from .utils import humanize_price

stripe.api_key = settings.STRIPE_SECRET_KEY

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'pk_test_ien1NqbAQfLtyz5PP7PWs15U00Rl8V9d74'

# You can find your endpoint's secret in your webhook settings
endpoint_secret = 'whsec_NoUa3aBmRfbFvcr8w4fogFf2WfKwGw3E'


def charge(request, price, title, user):
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=price,
                currency='eur',
                description=_('Diventi charge for %(title)s') % { 'title': title },
                source=request.POST['stripeToken'],
            )
            outcome = 1 # Success charge
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
            msg = _('Rate limit error')
            outcome = 0
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            msg = _('Invalid request error')
            outcome = 0
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            msg = _('Api authentication error')
            outcome = 0
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            msg = _('Api connection error')
            outcome = 0
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            msg = _('Generic error')
            outcome = 0
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            msg = _('Unexpected error')
            outcome = 0
        msg = _('You paid %(price)s for %(title)s') % {'price': humanize_price(price), 'title': title,}
        send_mail(
            _('Diventi: %(title)s purchase') % {'title': title,},
            _('Dear %(user)s, you have successufully purchased %(title)s for %(price)s.') % {
                'user': user.get_short_name(), 
                'price': price, 
                'title': title,
            },
            'info@playdiventi.it',
            [user.email],
            fail_silently=False,
        )
        payment = {
            'outcome': outcome,
            'msg': msg,
        }
        return payment
    else:
        return None