from django.db import models

# Create your models here.
from src.apps.account.models import User

# related_name  u
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField("Описание")
    image = models.ImageField("Картинка", upload_to="post/image/")

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Время добавления", auto_now=True)
    is_archived = models.BooleanField("Архивирован", default=False)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"#{self.id}-{self.description[:50]}"
    
class Comment(models.Model):  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.comments
       







