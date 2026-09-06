from functools import wraps

from machina.apps.forum_member.models import ForumProfile
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Post

from diventi.products.models import Product, ProductCategory
from diventi.feedbacks.models import Survey
from diventi.comments.models import DiventiComment
from diventi.blog.models import Article

from .models import Award, DiventiUser


def get_user_data(user, self=None):
    """
    Fetches user related objects cleanly.
    Reused across profile detail views and side drawers.
    """
    user_id = user.pk
    
    # 1. Recupero Collezioni e Progetti in un'unica valutazione
    surveys = Survey.objects.user_collection(user)
    collection = Product.objects.user_collection(user=user)
    
    # Valutiamo i progetti d'autore usando prefetch_basic per evitare query pesanti
    projects_qs = Product.objects.user_authored(user=user)
    projects_count = projects_qs.count()
    has_user_authored = projects_count > 0

    if has_user_authored:
        projects = projects_qs
        projects_categories = ProductCategory.objects.authored(user=user)        
    else:
        projects = Product.objects.none()
        projects_categories = ProductCategory.objects.none()

    # 2. Achievement: select_related solo sul deed (evitiamo la JOIN ridondante sull'utente)
    achievements = Award.objects.filter(awarded_user=user).select_related('deed')
    achievements_count = achievements.count()

    # 3. Commenti e Articoli
    comments_count = DiventiComment.objects.filter(user=user).count()
    
    articles = Article.objects.filter(author=user).order_by('-publication_date')
    articles_count = articles.count()
    recent_articles = articles[:3]

    # 4. Forum Machina Integrato
    try:
        forum_posts = ForumProfile.objects.get(user=user).posts_count
    except ForumProfile.DoesNotExist:
        forum_posts = 0

    recent_posts = Post.objects.none()
    if self and hasattr(self.request, 'forum_permission_handler'):
        forums = self.request.forum_permission_handler.get_readable_forums(
            Forum.objects.all(), 
            self.request.user,
        )
        recent_posts = (
            Post.approved_objects
            .select_related('topic', 'topic__forum')
            .filter(topic__forum__in=forums, poster=user)
            .order_by('-created')
        )[:3]

    return {
        'user_id': user_id,
        'surveys': surveys,
        'projects': projects,
        'projects_count': projects_count,
        'projects_categories': projects_categories,
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


def can_playtest(user): 
    return user.has_perm('accounts.can_playtest')