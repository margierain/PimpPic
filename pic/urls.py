from django.conf.urls import url, include
from views import (
    FolderApiView,
    SingleFolderAPIView, ImageApiView,
    SingleImageAPIView
)


urlpatterns = [
    url(r'^folders/$', FolderApiView.as_view(), name='folder-list'),
    url(r'^folders/(?P<id>\d+)/$',
        SingleFolderAPIView.as_view(), name='folder-detail'),
    url(r'^folders/(?P<id>\d+)/images/$',
        ImageApiView.as_view(), name='folder-photos'),
    url(r'^folders/(?P<id>\d+)/images/(?P<pk>\d+)/$',
        ImageApiView.as_view(), name='photo_in_folder'),
    url(r'^images/$', ImageApiView.as_view(), name='image-list'),
    url(r'^images/(?P<id>\d+)/$', SingleImageAPIView.as_view(), name='single-image'),
 

]
