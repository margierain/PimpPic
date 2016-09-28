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
    print('hvgcbnxbvhbn')
    print(thumbnail_url)

    class Meta:
        model = Photo
        fields = ('id', 'image', 'edited_image', 'title',
                  'effects', 'share_image', 'uploader', 'folder', 'thumbnail_url')
        read_only_fields = ('id', 'uploader', 'share_image', 'share_image',
                            'edited_image')
        # write_only_fields = ('image', 'image_thumbnail',)


class FolderSerializer(TimeStampMixinSerializer):
    images = ImageSerializer(many=True, read_only=True)
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Folder
        fields = ('id', 'name', 'creator', 'images')
        read_only_fields = ('creator', 'id',)
