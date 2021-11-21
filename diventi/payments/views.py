import stripe

from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from diventi.products.models import Product

from diventi.products.utils import (
    add_product_to_user_collection,
    humanize_price,
)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET_KEY
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        item = stripe.checkout.Session.list_line_items(session['id'], limit=1)['data'][0]
        user = get_object_or_404(
            get_user_model(), 
            nametag = session['client_reference_id'],
        )
        product = get_object_or_404(
            Product, 
            stripe_product=item['price']['product'],
        )        
        translation.activate(user.language)
        request.LANGUAGE_CODE = translation.get_language()
        add_product_to_user_collection(product, user)
        price = humanize_price(float(session['amount_total']))
        send_mail(
            _('Diventi: %(title)s purchase') % {'title': product.title,},
            _('Dear %(user)s, you have successufully purchased %(title)s for %(price)s.') % {
                'user': user.first_name,
                'price': price,
                'title': product.title,
            },
            'info@playdiventi.it',
            [user.email],
            fail_silently=False,
        )
    return HttpResponse(status=200)
