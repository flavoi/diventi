from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import translation

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from diventi.accounts.models import Award


class Command(BaseCommand):
    help = _('Send an email to all users that have received a new award')

    def handle(self, *args, **options):
        awards = Award.objects.to_be_notified()
        for a in awards:
            translation.activate(a.awarded_user.language)
            a.notified = True

            from_email = 'autori@playdiventi.it'
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr((str(Header('Diventi', 'utf-8')), from_email))
            html = _('Dear %(user)s,\nyour new %(deed)s tag is now available on your playdiventi.it profile.\n\nRegards,\nDiventi team') % {
                    'user': a.awarded_user.first_name,
                    'deed': a.deed,
                }
            msg.attach(MIMEText(html, 'html'))

            send_mail(
                subject = _('A new award from Diventi Roleplaying Community'),
                message = None,          
                from_email = from_email,
                recipient_list = [a.awarded_user.email,],
                fail_silently = False,
                html_message = msg.as_string(),
            )
            a.save()
            self.stdout.write(self.style.SUCCESS(_('Successfully notified award "%s"') % a))