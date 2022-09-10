import os
from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from config.models import CreationModificationDateBase

# user table
class User(models.Model):
    name = models.CharField(max_length=10)
    birthday = models.DateTimeField()
    phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_use_at = models.DateTimeField(auto_now=True)
    last_use_station = models.TextField()
    total_use = models.IntegerField()
    accident = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

# image table
class ImageModel(CreationModificationDateBase):
    image = models.ImageField(_("image"), upload_to='images')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])