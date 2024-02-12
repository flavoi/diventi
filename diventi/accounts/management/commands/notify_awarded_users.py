from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from diventi.accounts.models import Award


class Command(BaseCommand):
    help = _('Send an email to all users that have received a new award')

    def handle(self, *args, **options):
        awards = Award.objects.to_be_notified()
        for a in awards:
            a.notified = True
            send_mail(
                _('Diventi: new deed award'),
                _('Dear %(user)s, you have been awarded with a new deed! Enjoy your new %(deed)s achievement. Regards, Diventi\'s team') % {
                    'user': a.awarded_user.first_name,
                    'deed': a.deed,
                },
                'info@playdiventi.it',
                [a.awarded_user.email,],
                fail_silently=False,
            )
            a.save()
            self.stdout.write(self.style.SUCCESS('Successfully notified award "%s"' % a))