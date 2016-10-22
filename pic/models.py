from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.


class TimeStampMixin(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Folder(TimeStampMixin):
    name = models.CharField(max_length=100, default="untitled")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_modified']
        unique_together = ('name', 'creator')

    def get_no_of_images(self):
        return len(self.images.all())

    def __str__(self):
        return '{}, has {} photos'.format(self.name, self.get_no_of_images())


class Photo(TimeStampMixin):
    """Image model contains picture data and fields. """
    image = models.ImageField(upload_to='original', blank=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(300, 150)],
                                     format='JPEG',
                                     options={'quality': 60})
    edited_image = models.ImageField(upload_to='edited', blank=True)
    effects = models.CharField(max_length=100, blank=True)
    share_image = models.CharField(max_length=50, default="")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, null=True, blank=True, default="",
        related_name='images')

    class Meta:
        ordering = ['date_modified']

    # def image_thumbnail_url(self):
    #     return self.image_thumbnail.url

    def __str__(self):
        return self.effects

    def __unicode__(self):
        return unicode(self.effects)    
