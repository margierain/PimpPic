from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.urlresolvers import reverse
import time
import json, os
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
from django.contrib.auth import login
from social.apps.django_app.utils import load_backend, load_strategy, psa
from social.apps.django_app.views import _do_login
from .effect_processing import *
# Create your views here.

@psa('social:complete')
def fb_auth_token(request, backend):
    import ipdb; ipdb.set_trace()
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        print(user)
        print('marg')
        return user


class Register(APIView):
    """Handle GET to /api/register/(?P<backend>[^/]+)/
    GET:
        Returns login status
    """
    permission_classes = (AllowAny,)

    def get(self, request, backend, *args, **kwargs):
        user = fb_auth_token(request, backend)
        url = redirect_url = "social:complete"
        if url and not url.startswith('/'):
            url = reverse(redirect_url, args=(backend,))
        if user:
            login(request, user)
            strategy = load_strategy(request)
            backend = load_backend(strategy, backend, url)
            _do_login(backend, user, user)
            return Response("Login Successful!")
        else:
            return Response("Bad Credentials, check the Token and/or the UID", status=403)

class ImagePreview(View):

    def post(self, request, *args, **kwargs):
        img_id = request.POST.get('img_id', 0)
        effects = request.POST.get('effects', '')
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
        share_id = request.GET.get('share_id', None)
        response_data = {}
        if share_id:
            photo = Photo.objects.filter(share_image=share_id).first()
            if photo:
                serializer = ImageSerializer(photo)
                response_data = serializer.data

        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json")


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

    # before create
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
        folder_id = self.request.POST.get('folder_id', 0)
        folder = Folder.objects.filter(
            creator=self.request.user, id=folder_id).first()
        img_code = int(time.time())
        if folder:
            instance = serializer.save(
                creator=self.request.user, share_image=img_code)
        instance = serializer.save(
            creator=self.request.user, folder=folder, share_image=img_code)
        instance.file_size = int(instance.image.size / 1000)
        instance.save()

    def get_queryset(self):
        folder_id = self.kwargs.get('id', -1)
        if int(folder_id) == 0:
            return Photo.objects.filter(uploader=self.request.user, folder=None)
        folder = Folder.objects.filter(id=folder_id)
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
