from django.urls import path

from .views import ListFilesAPI, ReadUpdateDeleteFileAPI, UploadFileAPI

urlpatterns = [
    path('files/upload', UploadFileAPI.as_view(), name='upload-file'),
    path('files/<str:fileId>', ReadUpdateDeleteFileAPI.as_view(), name='read-update-delete-file'),
    path('files', ListFilesAPI.as_view(), name='list-files'),
]