from reviews.models import Review

from diventi.products.models import Product
from diventi.feedbacks.models import Survey
from diventi.comments.models import DiventiComment

from .models import (
    Achievement,
    DiventiUser,
)


"""
    Fetches user related objects.
    Is can be reused across multiple user views
"""
def get_user_data(user):    
    surveys = Survey.objects.user_collection(user)
    collection = Product.objects.user_collection(user=user)
    projects_count = user.collection.count
    survey_answers_count = user.answers.count
    ratings_count = Review.objects.filter(user=user).count()
    achievements = user.achievements.all()
    achievements_count = user.achievements.count
    locked_achievements = Achievement.objects.all().exclude(pk__in=achievements)
    comments_count = DiventiComment.objects.filter(user=user).count()
    has_user_authored = Product.objects.has_user_authored(user=user)
    user_data = {
        'surveys': surveys,
        'projects_count': projects_count,
        'survey_answers_count':  survey_answers_count,
        'ratings_count': ratings_count,
        'achievements_count': achievements_count,
        'achievements': achievements,
        'locked_achievements': locked_achievements,
        'comments_count': comments_count,
        'has_user_authored': has_user_authored,
        'collection': collection,
    }
    return user_data