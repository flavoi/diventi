from django.db import models
from django.conf import settings

from cuser.middleware import CuserMiddleware


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` field.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PromotableModel(models.Model):
    """
    An abstract base class model that enables a promotion feature
    similar to a facebook like on any model.
    """
    promotions = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def user_has_promoted(self):
        # Fetch the logged user thanks to a dedicated middleware
        user = CuserMiddleware.get_user() 
        if user in self.promotions.all():
            return True
        else:
            return False

    class Meta:
        abstract = True
