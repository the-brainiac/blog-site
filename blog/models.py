from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django_resized import ResizedImageField

class Blog(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    description = models.CharField(
        max_length = 500,
        validators=[MinLengthValidator(20, "Description must be greater than 20 characters")]
    )
    body = RichTextUploadingField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Comments
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')
    # Picture
    thumbnail = ResizedImageField(upload_to="images")

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_blogs')
    
    # Shows up in the admin list
    def __str__(self):
        return self.title

    def comment_count(self):
        return Comment.objects.filter(blog=self).count()

    def fav_count(self):
        return Fav.objects.filter(blog=self).count()

    # This returns the total sum of comments and likes of one blog to decide Trending Blog
    def trending_blog(self):
        return Comment.objects.filter(blog=self).count() + Fav.objects.filter(blog=self).count()



class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

class Fav(models.Model) :
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('blog', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.blog.title[:10])