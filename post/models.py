import uuid
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse

from notifications.models import Notification, Notification_StartUp


# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Tag(models.Model):
	title = models.CharField(max_length=75, verbose_name='Tag')
	slug = models.SlugField(null=False, unique=True)

	class Meta:
		verbose_name='Tag'
		verbose_name_plural = 'Tags'

	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])
		
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)


 

class PostFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
	file = models.FileField(upload_to=user_directory_path)


class Post(models.Model):

	AVAILABILITY_CATEGORY = [
    ('Available', 'Available'),
	('Not Available', 'Not Available')
]

	CLASS_CATEGORY = [
    ('Depression', 'Depression'),
    ('Anxiety disorders', 'Anxiety disorders'),
    ('Postpartum depression', 'Postpartum depression'),
    ('Postpartum anxiety', 'Postpartum anxiety'),
    ('Premenstrual dysphoric disorder', 'Premenstrual dysphoric disorder'),
    ('Eating disorders', 'Eating disorders'),
    ('Borderline personality disorder', 'Borderline personality disorder'),
    ('Obsessive-compulsive disorder', 'Obsessive-compulsive disorder'),
    ('Trauma-related disorders', 'Trauma-related disorders'),
    ('Bipolar disorder', 'Bipolar disorder'),
    ('Body dysmorphic disorder', 'Body dysmorphic disorder'),
    ('Perinatal mood & anxiety', 'Perinatal mood & anxiety'),
    ('Seasonal affective disorder', 'Seasonal affective disorder'),
    ('Substance use disorders', 'Substance use disorders'),
    ('Self-harm behaviors', 'Self-harm behaviors'),
    ('Dissociative disorders', 'Dissociative disorders'),
    ('Adjustment disorders', 'Adjustment disorders'),
    ('Psychotic disorders', 'Psychotic disorders')
]




	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	content =  models.ManyToManyField(PostFileContent, null=True, blank=True,  related_name='contents')
	lessonLink = models.URLField(max_length=200, null=True, blank=True, verbose_name='youtube.com', default='youtube.com')
	# codeSourceOfTheProject = models.URLField(max_length=200, null=True, blank=True, verbose_name='github.com', default='github.com')
	codeSourceOfTheProject = models.TextField( null=True,  blank=True, choices=AVAILABILITY_CATEGORY)
	authorOfTheVideo = models.TextField(max_length=50, verbose_name='authorOfTheVideo')
	caption = models.TextField(max_length=250, verbose_name='Caption')
	classCategory = models.TextField( null=True,  blank=True, choices=CLASS_CATEGORY)
	posted = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, related_name='tags')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	illustrated = models.IntegerField(default=1)
	instructed = models.IntegerField(default=1)
 

	def get_absolute_url(self):
		return reverse('postdetails', args=[str(self.id)])

	def __str__(self):
		return str(self.id)
 

class Follow(models.Model):
	follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
	following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')

	def user_follow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following
		notify = Notification(sender=sender, user=following, notification_type=3)
		notify.save()

	def user_unfollow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following

		notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
		notify.delete()

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
    	post = instance
    	user = post.user
    	followers = Follow.objects.all().filter(following=user)
    	for follower in followers:
    		stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
    		stream.save()
 
class Instructed(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_instructed')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_instructed')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()



class Illustrated(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_illustrated')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_illustrated')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()
 

#Stream
post_save.connect(Stream.add_post, sender=Post)
 

#Instructed
post_save.connect(Instructed.user_liked_post, sender=Instructed)
post_delete.connect(Instructed.user_unlike_post, sender=Instructed)

#Illustrated
post_save.connect(Illustrated.user_liked_post, sender=Illustrated)
post_delete.connect(Illustrated.user_unlike_post, sender=Illustrated)


#Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)