from .models import DiventiUser

from diventi.products.models import Product
from diventi.feedbacks.models import Survey


"""
    Utility method that fetch user related objects.
    Is is reused across multiple user views
"""
def get_user_data(context, user, loggeduser=None):
    achievements = user.achievements.all()
    context['achievements'] = achievements
    surveys = Survey.objects.user_collection(user)
    context['surveys'] = surveys
    collection = Product.objects.user_collection(user=user)
    PUBLIC_FIELDS = [
        'id', 'title', 'slug', 'category__title', 'description', 'image', 'file', 'available', 'courtesy_message', 'created', 'modified'
    ]
    if loggeduser and loggeduser != user:
        PUBLIC_FIELDS.remove('file')
    collection = collection.values(*PUBLIC_FIELDS)
    context['collection'] = collection
    return context