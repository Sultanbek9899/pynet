from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_MEN = "m"
    GENDER_WOMEN = "w"
    GENDER_CHOISES = (
        (GENDER_MEN, "Мужчина"),
        (GENDER_WOMEN, "Женщина"),
    )

    first_name=models.CharField("Имя", max_length=200, null=True,blank=True)
    last_name=models.CharField("Фамилия", max_length=200, null=True,blank=True)
    email = models.EmailField("Email", unique=True)
    about = models.TextField("О себе", null=True,blank=True)
    avatar = models.ImageField(
        "Аватарка",
          upload_to="user/images/", 
          null=True,blank=True
          )
    mobile = models.CharField("Номер телефона", max_length=15, null=True,blank=True)
    gender = models.CharField("Пол", max_length=2, choices=GENDER_CHOISES, null=True, blank=True)
    birthday = models.DateField("Дата рождения",null=True,blank=True)
    followers = models.ManyToManyField("self", related_name="followings", symmetrical=False)
    is_private = models.BooleanField("Закрытый аккаунт", default=True)
    last_login = models.DateTimeField("Последнее посещение", null=True, blank=True)


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def  __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_count')
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= 'Подписка'
        verbose_name= 'Подписки'
        ordering=['-created']

    def __str__(self):
        return f'{self.following} подписался на {self.follower}'