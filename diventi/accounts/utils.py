from .models import DiventiUser

from diventi.products.models import Product


"""
    Utility method that fetch user related objects.
    Is is reused across multiple user views
"""
def get_user_data(context, user, loggeduser=None):
    achievements = user.achievements.all()
    context['achievements'] = achievements
    collection = Product.objects.user_collection(user=user)
    if loggeduser and loggeduser != user:
        PUBLIC_FIELDS = [
            'title', 'slug', 'category', 'description', 'image'
        ]
        collection = collection.values(*PUBLIC_FIELDS)
    context['collection'] = collection
    return context