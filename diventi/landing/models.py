from django.db import models
from django.contrib.auth.models import AbstractUser


class DiventiUser(AbstractUser):
	email = models.EmailField(unique=True)
	avatar = models.ImageField(blank=True, upload_to='avatars/')
	bio = models.TextField(blank=True)
	role = models.CharField(blank=True, max_length=70)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def clean(self):
		# Set email as username to prevent validation errors.
		self.username = self.email