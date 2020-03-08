from django.http import HttpResponse
from django.conf import settings


def file_challenge(request):
    f = open(settings.BASE_DIR / 'brave/challenges' / request.LANGUAGE_CODE / 'brave-rewards-verification.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")
