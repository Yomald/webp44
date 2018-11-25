# Generated by Django 2.1.2 on 2018-11-25 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_remove_member_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='_member_likes_+', to='mainapp.Member'),
        ),
    ]
