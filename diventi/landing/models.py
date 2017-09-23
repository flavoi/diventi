from django.db import models

from ckeditor.fields import RichTextField


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