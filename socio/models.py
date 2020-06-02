from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# # Create your models here.

class Post(models.Model):
	image=models.ImageField(default="default_foo.png",upload_to="post_picture")
	title=models.CharField(max_length=100)
	caption=models.TextField()
	link=models.URLField(blank=True,default="")
	likes=models.ManyToManyField(User,related_name='likes',blank=True)
	
	date_posted=models.DateTimeField(default=timezone.now)
	author=models.ForeignKey(User , on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.author.username}\'s Post- {self.title}'

	def likecount(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)
		if img.height > 500 or img.width > 500:
			output_size = (500, 500)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Profile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	profile_image=models.ImageField(default="default.png",upload_to="profile_pics")

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.profile_image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.profile_image.path)