from rest_framework.permissions import BasePermission
from pic.models import Folder, Photo


class IsOwner(BasePermission):
    """
    Object-level permission class to allow only an Owner to edit their images else read only"""

    def has_object_permission(self, request, view, obj):
        if type(obj) is Photo:
            return obj.uploader == request.user
        return obj.creator == request.user 