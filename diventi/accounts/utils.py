from .models import DiventiUser

from diventi.products.models import Product
from diventi.feedbacks.models import Survey


"""
    Fetches user related objects.
    Is can be reused across multiple user views
"""
def get_user_data(context, user, loggeduser=None):
    achievements = user.achievements.all()
    context['achievements'] = achievements
    surveys = Survey.objects.user_collection(user)
    context['surveys'] = surveys
    collection = Product.objects.user_collection(user=user)
    context['collection'] = collection
    return context