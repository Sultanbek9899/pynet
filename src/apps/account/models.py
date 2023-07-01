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
