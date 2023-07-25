from django.db import models
from django.utils import timezone
from src.apps.account.models import User
from django.contrib.auth import get_user_model

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)         

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'custom_hashtag_table'
        ordering = ['name']
        
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField("Пост")
    image = models.ImageField("Картинка", upload_to="post/image/", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Время обновления", auto_now=True)
    is_archived = models.BooleanField("Архивирован", default=False)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    repost_set = models.ManyToManyField(User, through='Repost', related_name='reposted_posts')
    hashtags = models.ManyToManyField(Hashtag, related_name='posts')

    

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
    

    def __str__(self):
        return f"#{self.id}-{self.description[:50]}"
    
class Comment(models.Model):
    comments = models.TextField()
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.comments
       


class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reposted_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Репост"
        verbose_name_plural = "Репосты"

