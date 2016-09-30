from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.urlresolvers import reverse
import time
import json
import os
from .permissions import IsOwner
from .serializers import FolderSerializer, ImageSerializer
from .models import Photo, Folder
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from .effect_processing import *
# Create your views here.


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client



class ImagePreview(APIView):
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        img_id = self.kwargs.get('id', 0)
        effects = request.POST.get('effects', '')
        if effects:
            effect_obj = json.loads(effects)
        photo = Photo.objects.filter(id=img_id).first()
        response_data = {'image': ''}
        if photo:
            image_processor = ImageProcessor(photo)
            image_processor.process(effect_obj)
            response_data = {'image': image_processor.preview(
            ), 'applied_effects': image_processor.applied_effects()}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json")


class SharePhoto(View):

    def get(self, request, *args, **kwargs):
        share_id = self.kwargs.get('id', 0)
        response_data = {}
        photo = Photo.objects.filter(pk=share_id).first()
        if share_id and photo:
            serializer = ImageSerializer(photo)
            response_data = serializer.data
            print(response_data)
        response_json = json.dumps(response_data)
        return HttpResponse(response_data["image"], content_type="application/json")


class FolderApiView(ListCreateAPIView):

    """
    Returns list of folders if you are doing a GET request.
    Creates new folder if you are doing a POST request.
    Method: GET
      Parameters:
          page  (optional)    default=1
      Response: JSON
    Method: POST
      Parameters:
          name  (required)
      Response: JSON
    """

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = Folder.objects.filter(creator=self.request.user)
        return queryset


class SingleFolderAPIView(RetrieveUpdateDestroyAPIView):

    """
    Returns individual folder detail if you are doing a GET request.
    Updates individual folder detail if you are doing a PUT request.
    Deletes individual folder detail if you are doing a DELETE request.
    Method: GET
    Response: JSON
    Method: PUT
      Parameters:
          name  (required)
      Response: JSON
    Method: DELETE
        Response: JSON
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'


class ImageApiView(ListCreateAPIView):

    """
    Returns list of photos if you are doing a GET request.
    Creates new photo if you are doing a POST request.
    Method: GET
      Parameters:
          page  (optional)    default=1
      Response: JSON
    Method: POST
      Parameters:
          image  (required)
      Response: JSON
    """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # import ipdb; ipdb.set_trace()
        folder_id = self.kwargs.get('id', 0)
        folder_id = self.request.POST.get('folder_id', 0)
        folder = Folder.objects.filter(
            creator=self.request.user, id=folder_id).first()
        img_code = str(time.time())
        if folder:
            instance = serializer.save(
                uploader=self.request.user, folder=folder,
                share_image=img_code)
        instance = serializer.save(
            uploader=self.request.user, share_image=img_code)
        instance.file_size = int(instance.image.size / 1000)
        instance.save()

    def get_queryset(self):
        folder_id = self.kwargs.get('id', 0)
        folder = Folder.objects.filter(id=folder_id).first()
        if(folder):
            image = Photo.objects.filter(
                uploader=self.request.user, folder=folder)
        else:
            image = Photo.objects.filter(uploader=self.request.user)
        return image


class SingleImageAPIView(RetrieveUpdateDestroyAPIView):

    """
    Returns individual photo detail if you are doing a GET request.
    Updates individual photo detail if you are doing a PUT request.
    Deletes individual photo detail if you are doing a DELETE request.
    Method: GET
    Response: JSON
    Method: PUT
      Parameters:
          title  (required)
      Response: JSON
    Method: DELETE
        Response: JSON
    """
    queryset = Photo.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()
        image_processor = ImageProcessor(instance)
        if instance.effects:
            effect_obj = json.loads(instance.effects)
            image_processor.process(effect_obj)
            edited_path = image_processor.save()
            instance.edited_image = edited_path
            instance.save()

    def perform_destroy(self, instance):
        """Checks if the file exists and change the file name to edited"""
        if(os.path.isfile(instance.image.path)):
            os.remove(instance.image.path)

        if(os.path.isfile(instance.image.path.replace('original', 'edited'))):
            os.remove(instance.image.path.replace('original', 'edited'))
        instance.delete()
