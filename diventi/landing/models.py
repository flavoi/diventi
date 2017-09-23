from django.db import models
from django.contrib.auth.models import AbstractUser

from ckeditor.fields import RichTextField


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


class Profile(models.Model):
	title = models.CharField(max_length=50)
	abstract = RichTextField()
	description = RichTextField()
	image = models.ImageField(blank=True, upload_to='landing/')
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.title


class Feature(models.Model):
	COLORS_CHOICES = (
		('info', 'Blue'),
		('primary', 'Rose'),
		('danger', 'Red'),
		('success', 'Green'),
		('default', 'Gray'),	   
	)

	icon = models.CharField(max_length=30)
	title = models.CharField(max_length=50)
	description = RichTextField()
	color = models.CharField(choices=COLORS_CHOICES, max_length=30, default='default')
	profile = models.ForeignKey(Profile)

	def __str__(self):
		return self.title