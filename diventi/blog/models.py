from django.db import models

from tinymce.models import HTMLField


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` field.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    """
        Defines the main argument of any post.
    """
    title = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
    	verbose_name_plural = "categories"


class PostImage(models.Model):
    """
    	Decorates a Post with a beautiful image and its appropriate 
    	credits.
    """
    image = models.ImageField(blank=True, upload_to='media/diventi/')
    caption = models.CharField(max_length=60, blank=True)

    def __unicode__(self):
        return u'%s' % (self.caption)


class Post(TimeStampedModel):
    """
        Blog posts are built upon a specific category and are always 
        introduced by a nice heading picture.
    """
    title = models.CharField(max_length=60)
    category = models.ForeignKey(Category)
    image = models.ForeignKey(PostImage)
    content = HTMLField()
    published = models.BooleanField(default=False)
    publication_date = models.DateField(auto_now_add=True, null=True)
    hot = models.BooleanField(default=False)
    slug = models.SlugField()
    # author = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.title

    # Pubblication date is updated if published has been modified from False to True
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.old_published = self.published

    def save(self, *args, **kwargs):
        if self.old_published != self.published and self.published:
            self.publication_date = timezone.now()
        super(Post, self).save(*args, **kwargs)


class Attachment(models.Model):
    """
        Stores one or more files for a given Post.
    """
    title = models.CharField(max_length=60)
    file = models.FileField(upload_to='media/attachments/')
    post = models.ForeignKey(Post)

    def save(self, *args, **kwargs):
        if self.goal:
            self.bio = self.goal.bio
        super(Attachment, self).save(*args, **kwargs)