from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
from resizeimage import resizeimage
from io import BytesIO
from django.core.files.base import ContentFile

def get_image_path(instance, filename):
    return os.path.join('img', str(instance.id), filename)

class Article(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		pil_image_obj = Image.open(self.image)
		img_size = pil_image_obj.size
		if float(img_size[0]) >= 800:
			new_image = resizeimage.resize_width(pil_image_obj, 800)
			new_image_io = BytesIO()
			new_image.save(new_image_io, format='JPEG')
			temp_name = self.image.name
			self.image.delete(save=False)
			self.image.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)
		super(Article, self).save(*args, **kwargs)