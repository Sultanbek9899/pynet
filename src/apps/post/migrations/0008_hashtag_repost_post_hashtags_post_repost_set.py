# Generated by Django 4.2.2 on 2023-07-24 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0007_merge_20230723_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'custom_hashtag_table',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Repost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reposted_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reposts', to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Репост',
                'verbose_name_plural': 'Репосты',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(related_name='posts', to='post.hashtag'),
        ),
        migrations.AddField(
            model_name='post',
            name='repost_set',
            field=models.ManyToManyField(related_name='reposted_posts', through='post.Repost', to=settings.AUTH_USER_MODEL),
        ),
    ]