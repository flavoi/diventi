from reviews.models import Review

from machina.apps.forum_member.models import ForumProfile
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Post

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
def get_user_data(user, self=None):
    user_id = user.pk
    surveys = Survey.objects.user_collection(user)
    collection = Product.objects.user_collection(user=user)
    projects_count = user.collection.count
    survey_answers_count = user.answers.count
    ratings_count = Review.objects.filter(user=user).count()
    achievements = user.achievements.all()
    achievements_count = user.achievements.count
    achievements_total_count = Achievement.objects.all().count() 
    locked_achievements = Achievement.objects.all().exclude(pk__in=achievements)
    comments_count = DiventiComment.objects.filter(user=user).count()
    has_user_authored = Product.objects.has_user_authored(user=user)
    forum_posts = ForumProfile.objects.get(user=user).posts_count
    recent_posts = Post.objects.none()
    if self:
        forums = self.request.forum_permission_handler.get_readable_forums(
                Forum.objects.all(), self.request.user,
            )
        recent_posts = (
            Post.approved_objects
            .select_related('topic', 'topic__forum')
            .filter(topic__forum__in=forums, poster=user)
            .order_by('-created')
        )[:3]
    user_data = {
        'user_id': user_id,
        'surveys': surveys,
        'projects_count': projects_count,
        'survey_answers_count':  survey_answers_count,
        'ratings_count': ratings_count,
        'achievements_count': achievements_count,
        'achievements': achievements,
        'locked_achievements': locked_achievements,
        'achievements_total_count': achievements_total_count,
        'comments_count': comments_count,
        'has_user_authored': has_user_authored,
        'collection': collection,
        'forum_posts': forum_posts,
        'recent_posts': recent_posts,
    }
    return user_data
        