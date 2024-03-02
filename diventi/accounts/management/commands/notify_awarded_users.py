from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.utils import translation

from diventi.core.utils import send_diventi_email
from diventi.accounts.models import Award


class Command(BaseCommand):
    help = _('Send an email to all users that have received a new award')

    def handle(self, *args, **options):
        awards = Award.objects.to_be_notified()
        for a in awards:
            translation.activate(a.awarded_user.language)
            a.notified = True
            send_diventi_email(
                subject = _('A new award from Diventi Roleplaying Community'),
                message = None,          
                from_email = 'autori@playdiventi.it',
                recipient_list = [a.awarded_user.email,],
                from_name = 'Diventi',
                html_message = _('Dear %(user)s,<br />your new <b>%(deed)s</b> tag is now available on your playdiventi.it profile.<br/ ><br />Regards,<br />Diventi team') % {
                    'user': a.awarded_user.first_name,
                    'deed': a.deed,
                },
            )
            a.save()
            self.stdout.write(self.style.SUCCESS(_('Successfully notified award "%s"') % a))