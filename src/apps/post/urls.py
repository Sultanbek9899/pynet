from django.urls import path
from .views import get_posts, index, get_categories, create_comment

urlpatterns= [
    path('', index, name='index'), 
    path('post/lists/', get_posts, name='post_list'),
    path('categories/', get_categories, name='categories_list'),
    path('create_comment', create_comment, name='create_comment'),

]
