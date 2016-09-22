from django.shortcuts import render
from django.contrib.auth.models import User
import time
from .permissions import IsOwner
from .serializers import FolderSerializer, ImageSerializer
from .models import Image, Folder
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
# Create your views here.


class ImagePreview(View):

    def post(self, request, *args, **kwargs):
        img_id = request.POST.get('img_id', 0)
        effects = request.POST.get('effects', '')
        effect_obj = json.loads(effects)
        photo = Image.objects.filter(id=img_id).first()
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
            photo = Image.objects.filter(share_image=share_id).first()
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
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Folder.objects.filter(user=self.request.user)
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
            user=self.request.user, id=folder_id).first()
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
            return Image.objects.filter(uploader=self.request.user, folder=None)
        folder = Folder.objects.filter(id=folder_id)
        if(folder):
            image = Image.objects.filter(
                uploader=self.request.user, folder=folder)
        else:
            image = Image.objects.filter(uploader=self.request.user)
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
    queryset = Image.objects.all()
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
