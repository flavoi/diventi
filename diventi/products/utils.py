
# Returns the description of the last purchase
# Of none if none is found
def get_last_purchase_description(last_purchase):
    if last_purchase: 
        description = _('last purchase: %(last_sub)s on %(date_joined)s') % {
            'last_sub': last_purchase: last_purchase.customer.get_short_name(),
            'date_joined': naturalday(last_purchase.created),
        }
    else:
        description = None
    return description