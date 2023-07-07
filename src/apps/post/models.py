from django.db import models

# Create your models here.
from src.apps.account.models import User
from django.utils import timezone


# related_name  u
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField("Пост") 
    image = models.ImageField("Картинка", upload_to="post/image/", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Время добавления", auto_now=True)
    is_archived = models.BooleanField("Архивирован", default=False)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    
    # def total_likes(self):
    #      return self.likes.count
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"#{self.id}-{self.description[:50]}"

class Likes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

class Comments(models.Model):
    body= models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    
    
    def __str__(self):
            return '%s-%s' % (self.post.title, self.user.username)
    


    
       

