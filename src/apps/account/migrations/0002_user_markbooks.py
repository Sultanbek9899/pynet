# Generated by Django 4.2.2 on 2023-07-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_image'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='markbooks',
            field=models.ManyToManyField(to='post.post'),
        ),
    ]