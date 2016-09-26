from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TimeStampMixin, Folder, Photo
from rest_framework.serializers import (
    ModelSerializer,
)


class TimeStampMixinSerializer(ModelSerializer):

    class Meta:
        model = TimeStampMixin
        fields = ('date_created', 'date_modified')
        read_only_fields = ('date_created')


class ImageSerializer(TimeStampMixinSerializer):

    class Meta:
        model = Photo
        fields = ('id', 'image', 'image_thumbnail', 'edited_image', 'title',
                  'effects', 'share_image', 'uploader', 'folder')
        read_only_fields = ('id', 'uploader',)


class FolderSerializer(TimeStampMixinSerializer):
    images = ImageSerializer(many=True, read_only=True)
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Folder
        fields = ('id', 'name', 'creator', 'images')
        read_only_fields = ('creator', 'id',)
