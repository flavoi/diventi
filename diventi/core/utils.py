import unicodedata

# Format the price for human eyes
# Currency is defaulted to Euro
def humanize_price(price, sign='EURO SIGN'):
    p = ('%(currency)s %(price).2f' % {
        'currency': unicodedata.lookup('EURO SIGN'), 
        'price': price / 100,
    })
    return p