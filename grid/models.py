from django.db import models
from django.contrib.auth.models import User
import os

def get_image_path(instance, filename):
    return os.path.join('img', str(instance.id), filename)

class Article(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	def __str__(self):
		return self.name