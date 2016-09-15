from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.


class Image(models.Model):
    """Image model contains picture data and fields. """
    image = models.ImageField(upload_to='images')
    image = ProcessedImageField([ResizeToFit(1920, 1200, False)])
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(300, 150)],
                                     format='JPEG',
                                     options={'quality': 60})
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['date_modified']

    def __str__(self):
        return self.image


class EffectType(models.Model):
    """Model holding effect and filter types. """
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{0}'.format(self.name)


class Effect(models.Model):
    """Model holding effects and filters. """
    name = models.CharField(max_length=50)
    effect_type = models.ForeignKey(EffectType, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class Img_edited(models.Model):
    """Edited images model """
    image_name = models.ImageField('img', upload_to='edited_img/')
    effect = models.CharField(max_length=50)
    original_img = models.ForeignKey(Image, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_modified']

    def __str__(self):
        return '{} applied {} effect'.format(self.original_img, self.effect)
