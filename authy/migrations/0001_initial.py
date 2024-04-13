# Generated by Django 4.2.3 on 2023-07-29 14:20

import authy.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post_StartUp', '0001_initial'),
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='Team Member X', max_length=50)),
                ('last_name', models.CharField(default=' Y', max_length=50)),
                ('location', models.CharField(default='Location Z', max_length=50)),
                ('githubProfile', models.URLField(blank=True, default='github.com', null=True, verbose_name='githubProfile')),
                ('linkedInnProfile', models.URLField(blank=True, default='linkedin.com', null=True, verbose_name='linkedInnProfile')),
                ('interstCategory', models.TextField(choices=[('Language', 'Language'), ('Framework', 'Framework'), ('Web Project', 'Web Project'), ('Game Project', 'Game Project'), ('Mobile Project', 'Mobile Project'), ('AI Project', 'AI Project'), ('Algorithms', 'Algorithms'), ('Data Structures', 'Data Structures'), ('Data Science', 'Data Science'), ('Data Visualization', 'Data Visualization'), ('Programming General', 'Programming General')], default='Programming General')),
                ('created', models.DateField(auto_now_add=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=authy.models.user_directory_path, verbose_name='Picture')),
                ('favorites', models.ManyToManyField(to='post.post')),
                ('favorites_StartUp', models.ManyToManyField(to='post_StartUp.post_startup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
