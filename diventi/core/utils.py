import unicodedata, smtplib

from email.message import EmailMessage
from email.utils import formataddr

from django.conf import settings


# Format the price for human eyes
# Currency is defaulted to Euro
def humanize_price(price, sign='EURO SIGN'):
    p = ('%(currency)s %(price).2f' % {
        'currency': unicodedata.lookup('EURO SIGN'), 
        'price': price / 100,
    })
    return p


# Send an email using a set gmail account via smtp
def send_diventi_email(subject, message, from_email, recipient_list, from_name, html_message):
    server = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
    server.ehlo('Gmail')
    server.starttls()
    email_user = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD
    server.login(email_user,email_password)

    msg = EmailMessage()
    if html_message:
        msg.set_content(html_message, subtype='html')
    elif message:
        msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = formataddr((from_name, from_email))
        
    for r in recipient_list:
        msg['To'] = r
        server.send_message(msg)
    server.quit()
    return 1