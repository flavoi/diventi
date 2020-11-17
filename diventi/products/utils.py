import unicodedata


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

# Format the price for human eyes
# Currency is defaulted to Euro
def humanize_price(price, sign='EURO SIGN'):
    p = ('%(currency)s %(price).2f' % {
        'currency': unicodedata.lookup('EURO SIGN'), 
        'price': price / 100,
    })
    return p

# Adds a product to the user collection
def add_product_to_user_collection(product, user):
    if not product.user_has_already_bought(user):
        return product.customers.add(user)
    else:
        msg = _('The user has this product already.')
        raise Http404(msg)