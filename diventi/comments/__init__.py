default_app_config = 'diventi.comments.apps.CommentsConfig'

def get_model():
    from diventi.comments.models import DiventiComment
    return DiventiComment

def get_form():
    from diventi.comments.forms import DiventiCommentForm
    return DiventiCommentForm