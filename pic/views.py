from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from rest_framework import status
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
from .effect_processing import *


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
    permission_classes = (IsAuthenticated, IsOwner,)


    def perform_create(self, serializer):
        if serializer.is_valid:
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
    permission_classes = (IsAuthenticated, IsOwner,)

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
    permission_classes = (IsAuthenticated, IsOwner,)


    def perform_create(self, serializer):
        folder_id = self.kwargs.get('id', 0)
        folder_id = self.request.POST.get('folder_id', 0)
        folder = Folder.objects.filter(
            creator=self.request.user, id=folder_id).first()
        img_code = str(time.time())
        if serializer.is_valid:
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
    permission_classes = (IsAuthenticated, IsOwner,)
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()
        image_processor = ImageProcessor(instance)
        if instance.effects:
            effect_obj = instance.effects
            image_processor.process(effect_obj)
            edited_path = image_processor.save()
            edited_path = edited_path.replace('/media/', '')
            instance.edited_image = edited_path
            instance.save()

    def perform_destroy(self, instance):
        """Checks if the file exists and change the file name to edited"""
        if(os.path.isfile(instance.image.path)):
            os.remove(instance.image.path)

        if(os.path.isfile(instance.image.path.replace('original', 'edited'))):
            os.remove(instance.image.path.replace('original', 'edited'))
        instance.delete()

