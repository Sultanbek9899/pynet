from django.db import models
from src.apps.account.models import User
from django.utils import timezone

# class Category(models.Model):
#     name=models.CharField(max_length=255)
#     slug=models.SlugField(max_length=255)
#     class Meta:
#         verbose_name='Категория'
#         verbose_name_plural='Категории'

#     def __str__(self):
#         return self.name  
    
class Post(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='author' )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        def __str__(self):
            return self.title


class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post
            