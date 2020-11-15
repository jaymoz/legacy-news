from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField
from embed_video.fields import EmbedVideoField

User = get_user_model()

class PostView(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username



class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField()

	def __str__(self):
		return self.user.username


class Category(models.Model):
	title = models.CharField(max_length=40)
	slug = models.SlugField(blank=True, null=True)
	thumbnail = models.ImageField(blank=True, null=True)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return  reverse('category-detail',kwargs={'slug':self.slug})



class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	post = models.ForeignKey(
		'Post', related_name='comments', on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username



class Post(models.Model):
	title = models.CharField(max_length=150)
	overview = models.CharField(max_length=2000)
	timestamp = models.DateTimeField(auto_now_add=True)
	comment_count = models.IntegerField(default=0)
	content = HTMLField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	thumbnail = models.ImageField()
	categories = models.ManyToManyField(Category)
	featured = models.BooleanField()
	previous_post = models.ForeignKey('self',on_delete=models.SET_NULL, blank=True, null=True, related_name='last_post')
	next_post = models.ForeignKey('self',on_delete=models.SET_NULL, blank=True, null=True,related_name='next1_post')
	video = EmbedVideoField(blank=True, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return  reverse('post-detail',kwargs={'id':self.id})

	def get_update_url(self):
		return  reverse('post-detail',kwargs={'id':self.id})

	def get_delete_url(self):
		return  reverse('post-detail',kwargs={'id':self.id})

	@property
	def get_comments(self):
		return self.comments.all().order_by('-timestamp')

	@property
	def view_count(self):
		return PostView.objects.filter(post=self).count()

	@property
	def comment_count(self):
		return Comment.objects.filter(post=self).count()


class TeamInfo(models.Model):
	full_name = models.CharField(max_length=150)
	title = models.CharField(max_length=150)
	description = HTMLField()
	image = models.ImageField(default='user.svg',null=True, blank=True)
	facebook_link = models.CharField(max_length=500,null=True,blank=True)
	instagram_link = models.CharField(max_length=500, null=True, blank=True)
	twitter_link = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.full_name

class Contact(models.Model):
	name = models.CharField(max_length=150)
	email = models.EmailField()
	message = HTMLField()

	def __str__(self):
		return self.email

class Images(models.Model):
	homepage = models.ImageField( blank=False,null=False)
	about_images1 = models.ImageField( blank=False,null=False)
	about_images2 = models.ImageField(blank=False,null=False)
	about_images3 = models.ImageField(blank=False,null=False)
	blog_background_image = models.ImageField( blank=False,null=False)
	contact_background_image = models.ImageField( blank=False,null=False)

	class Meta:
		verbose_name_plural = 'Images'


class FooterLinks(models.Model):
	footer_text = models.CharField(max_length=200, blank=True, null=True)
	facebook_link = models.CharField(max_length=500,null=True,blank=True)
	instagram_link = models.CharField(max_length=500, null=True, blank=True)
	twitter_link = models.CharField(max_length=500, null=True, blank=True)


	class Meta:
		verbose_name_plural = 'FooterLinks'


class HomepageAboutText(models.Model):
	website_name_on_homepage = models.CharField(max_length=150, blank=True, null=True)
	about = HTMLField(blank=True, null=True)

	