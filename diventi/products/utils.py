import stripe, boto3
from django.http import Http404, HttpResponse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturalday

from botocore.exceptions import ClientError

from diventi.core.utils import (
    humanize_price,
)


# Returns the description of the last purchase
# Of none if none is found
def get_last_purchase_description(last_purchase):
    if last_purchase: 
        description = _('last purchase: %(last_sub)s on %(date_joined)s') % {
            'last_sub': last_purchase.customer.get_short_name(),
            'date_joined': naturalday(last_purchase.created),
        }
    else:
        description = None
    return description

# Adds a product to the user collection
def add_product_to_user_collection(product, user):
    if not product.user_has_already_bought(user):
        return product.customers.add(user)
    else:
        msg = _('The user has this product already.')
        raise Http404(msg)

# Adds all products of a package to the user collection
def add_package_to_user_collection(package, user):
    for product in package.related_products.all():
        if not product.user_has_already_bought(user):
            add_product_to_user_collection(product, user)
    

# Get relevant data for the selected product
def get_product_context(request, product):
    if product.unfolded:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_price = stripe.Price.retrieve(product.stripe_price)
        price = humanize_price(float(stripe_price['unit_amount_decimal']))
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        user_has_already_bought = product.user_has_already_bought(request.user)
        context = {
            'price': price,
            'stripe_publishable_key': stripe_publishable_key,
            'user_has_already_bought': user_has_already_bought,
        }
    else:
        context = {}
    return context


def get_s3_safe_url(product):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
    )
    
    try:
        response_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': product.file.name},
            ExpiresIn=3600
        )
        return response_url
    except ClientError:
        return HttpResponse(_("S3 error"), status=500)
