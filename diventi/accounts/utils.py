from .models import DiventiUser

from diventi.products.models import Product


"""
    Utility method that fetch user related objects.
    Is is reused across multiple user views
"""
def get_user_data(context, user):
    achievements = user.achievements.all()
    print(achievements)
    context['achievements'] = achievements
    collection = Product.objects.user_collection(user=user)
    context['collection'] = collection
    return context