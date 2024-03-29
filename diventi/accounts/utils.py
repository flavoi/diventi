from reviews.models import Review

from machina.apps.forum_member.models import ForumProfile
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Post

from diventi.products.models import (
    Product,
    ProductCategory
)
from diventi.feedbacks.models import Survey
from diventi.comments.models import DiventiComment
from diventi.blog.models import Article

from .models import (
    Award,
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
    has_user_authored = Product.objects.has_user_authored(user=user)    
    if has_user_authored:
        projects = Product.objects.user_authored(user=user)
        projects_count = projects.count()
        projects_categories = ProductCategory.objects.authored(user=user)        
    else:
        projects = Product.objects.none()
        projects_count = 0
        projects_categories = ProductCategory.objects.none()
    ratings_count = Review.objects.filter(user=user).count()
    achievements = Award.objects.filter(awarded_user=user).related()
    achievements_count = achievements.count()
    comments_count = DiventiComment.objects.filter(user=user).count()
    articles = (
        Article.objects
        .filter(author=user)    
        .order_by('-publication_date')
        )
    articles_count = articles.count()
    recent_articles = articles[:3]
    try:
        forum_posts = ForumProfile.objects.get(user=user).posts_count
    except ForumProfile.DoesNotExist:
        forum_posts = 0
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
        'projects': projects,
        'projects_count': projects_count,
        'projects_categories': projects_categories,
        'ratings_count': ratings_count,
        'achievements_count': achievements_count,
        'achievements': achievements,
        'comments_count': comments_count,
        'has_user_authored': has_user_authored,
        'collection': collection,
        'collection_count': len(collection),
        'forum_posts': forum_posts,
        'recent_posts': recent_posts,
        'recent_articles': recent_articles,
        'articles_count': articles_count,
    }
    return user_data
        