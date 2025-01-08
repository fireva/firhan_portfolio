from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.utils.text import Truncator

class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='profile_photos/')

class Experience(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(default="")
    link = models.URLField(blank=True, null=True)

class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date_created = models.DateTimeField(default=now)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)  # New field for likes
    dislikes = models.IntegerField(default=0)  # New field for dislikes
    def get_thumbnail(self):
        plain_text = strip_tags(self.content)
        paragraphs = plain_text.split("\n")
        first_paragraph = paragraphs[0] if paragraphs else plain_text
        return Truncator(first_paragraph).chars(400, truncate='...')  # Limit to 200 characters
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional name field
    content = models.TextField()
    date_created = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        # Default to 'Anonymous' if no name is provided
        if not self.name:
            self.name = "Anonymous"
        super().save(*args, **kwargs)