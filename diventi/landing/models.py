from django.db import models
from django.contrib.auth.models import AbstractUser


class DiventiUser(AbstractUser):
	avatar = models.ImageField(upload_to='avatars/')
	bio = models.TextField()
	role = models.CharField(max_length=70)