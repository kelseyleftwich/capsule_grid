from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
from resizeimage import resizeimage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_image_path(instance, filename):
    return os.path.join('img', slugify(instance.name), filename)

class Article(models.Model):
	ARTICLE_TYPES = (
		('T', 'Top'),
		('B', 'Bottom'),
		('O', 'Outer'),
		('D', 'Dress'),
		('A', 'Details'),
		('S', 'Shoes'),
		)

	WEATHER_TYPES = (
		('C', 'Cool'),
		('W', 'Warm'),
		('B', 'Both'),
		)

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	article_type = models.CharField(max_length=1, choices=ARTICLE_TYPES, null=True)
	weather_type = models.CharField(max_length=1, choices=WEATHER_TYPES, null=True)
	
	image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
	image_external = models.CharField(max_length=255, null=True, blank=True)

	def get_id(self):
		return self.id

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if self.image:
			pil_image_obj = Image.open(self.image)
			img_size = pil_image_obj.size
			if float(img_size[0]) > 500:
				new_image = resizeimage.resize_width(pil_image_obj, 500)
				new_image_io = BytesIO()
				new_image.save(new_image_io, format='JPEG')
				temp_name = self.image.name
				self.image.delete(save=False)
				self.image.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)
		super(Article, self).save(*args, **kwargs)

class Plan(models.Model):
	SEASON_TYPES = (
		('W','Winter'),
		('P','Spring'),
		('S','Summer'),
		('A','Autumn'),
		)

	name = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	season_type = models.CharField(max_length=1, choices=SEASON_TYPES, null=True)

	top_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(0)])
	bottom_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(0)])
	dress_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(0)])
	shoe_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(0)])
	details_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(0)])
	outer_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(0)])

	articles =  models.ManyToManyField(Article)

	def total(self):
		total = self.top_count + self.bottom_count + self.dress_count + self.shoe_count + self.details_count + self.outer_count
		return total

	def total_actual(self):
		return self.articles.all().count()

	def tops_actual(self):
		return self.articles.filter(article_type='T').count()

	def bottoms_actual(self):
		return self.articles.filter(article_type='B').count()

	def outer_actual(self):
		return self.articles.filter(article_type='O').count()

	def details_actual(self):
		return self.articles.filter(article_type='A').count()

	def dresses_actual(self):
		return self.articles.filter(article_type='D').count()

	def shoes_actual(self):
		return self.articles.filter(article_type='S').count()

	def __str__(self):
		return self.name


class Outfit(models.Model):
	name=models.CharField(max_length=255, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

	articles =  models.ManyToManyField(Article)

	def __str__(self):
		if not self.name:
			return "unnamed"
		else:
			return self.name

class Profile(models.Model):
	PROFILE_TYPES = (
		('F','Free'),
		('P','Paid'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_type = models.CharField(max_length=1, choices=PROFILE_TYPES, default='F')

	def __str__(self):
		return self.user.email + " " + self.profile_type


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)