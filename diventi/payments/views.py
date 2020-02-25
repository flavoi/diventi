import stripe

from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

def charge(request, price, title, user):
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=price,
                currency='eur',
                description='Diventi charge for {}'.format(title),
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
            print('Rate limit error')
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print('Invalid request error')
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print('Api authentication error')
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print('Api connection error')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            print('Generic error')
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            print('Unexpected error')
        message = _('You paid %(price)s for %(title)s') % {'price': price, 'title': title,}
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
            'outcome': 1,
            'msg': message,
        }
        return payment
    else:
        return None