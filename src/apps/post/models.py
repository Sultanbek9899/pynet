from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from src.apps.account.models import User


class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Посты"
        verbose_name_plural = "Посты"


    def __str__(self):
        return self.title
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    for_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replas')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Комментарии"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.for_post