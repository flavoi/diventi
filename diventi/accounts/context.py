"""
    Custom context processors for the accounts app.
    This script checks the user preferred language in every template.
"""

from django.utils import translation
from django.utils.translation import get_language

from reviews.models import Review

from .models import Achievement


def user_preferred_language(request):
    if request.user.is_authenticated:
        user_language = request.user.language
        current_language = get_language()        
        if user_language != current_language:
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return {'request': request}


def user_statistics(request):
	context = {}
	if request.user.is_authenticated:
		projects_count = request.user.collection.count
		survey_answers_count = request.user.answers.count
		ratings_count = Review.objects.filter(user=request.user).count()
		achievements_total_count = Achievement.objects.all().count()
		achievements_count = request.user.achievements.count
		user_achievements = Achievement.objects.filter(users=request.user)
		locked_achievements = Achievement.objects.all().exclude(pk__in=user_achievements)
		context = {
			'projects_count': projects_count,
			'survey_answers_count':  survey_answers_count,
			'ratings_count': ratings_count,
			'achievements_total_count': achievements_total_count,
			'achievements_count': achievements_count,
			'user_achievements': user_achievements,
			'locked_achievements': locked_achievements,
    	}
	return context