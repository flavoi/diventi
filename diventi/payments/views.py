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
from django.contrib import messages

from diventi.products.models import (
    Product,
)

from diventi.packages.models import (
    Package,
)

from diventi.core.utils import (
    humanize_price,
)

from diventi.products.utils import (
    add_product_to_user_collection,
    add_package_to_user_collection,
)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET_KEY
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    if not sig_header:
        return HttpResponse('This is a stripe webhook.')
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
        try:
            product = Product.objects.get(
                stripe_product=item['price']['product'],
            )
            receipt_title = product.title
            add_product_to_user_collection(product, user=user)
        except Product.DoesNotExist:
            package = get_object_or_404(
                Package,
                stripe_product=item['price']['product'],
            )
            receipt_title = package.title
            add_package_to_user_collection(package, user=user)
        translation.activate(user.language)
        request.LANGUAGE_CODE = translation.get_language()
        price = humanize_price(float(session['amount_total']))
        send_mail(
            _('Diventi: %(title)s purchase') % {'title': receipt_title,},
            _('Dear %(user)s,\nyou have successfully purchased %(title)s for %(price)s.\n\nRegards,\nDiventi team') % {
                'user': user.first_name,
                'price': price,
                'title': receipt_title,
            },
            'info@playdiventi.it',
            [user.email,],
            fail_silently=False,
        )
    return HttpResponse(status=200)
