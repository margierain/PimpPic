from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TimeStampMixin, Folder, Photo


class TimeStampMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeStampMixin
        fields = ('date_created', 'date_modified')
        read_only_fields = ('date_created')


class ImageSerializer(TimeStampMixinSerializer):
    thumbnail_url = serializers.CharField(
        source='image_thumbnail_url', read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'image', 'edited_image', 'effects',
                  'share_image', 'uploader', 'folder', 'thumbnail_url',
                  'date_created', 'date_modified')
        read_only_fields = ('id', 'uploader', 'share_image',
                            'edited_image', 'date_created', )


class FolderSerializer(TimeStampMixinSerializer):
    images = ImageSerializer(many=True, read_only=True)
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Folder
        fields = ('id', 'name', 'creator', 'images',
                  'date_created', 'date_modified')
        read_only_fields = ('creator', 'id', 'date_created',)
