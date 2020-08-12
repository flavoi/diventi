from .models import DiventiUser

from diventi.products.models import Product
from diventi.feedbacks.models import Survey

from .models import Achievement


"""
    Fetches user related objects.
    Is can be reused across multiple user views
"""
def get_user_data(context, user, loggeduser=None):
    achievements = user.achievements.all()
    context['achievements'] = achievements
    locked_achievements = Achievement.objects.all().exclude(pk__in=achievements)
    context['locked_achievements'] = locked_achievements
    surveys = Survey.objects.user_collection(user)
    context['surveys'] = surveys
    collection = Product.objects.user_collection(user=user)
    context['collection'] = collection
    return context