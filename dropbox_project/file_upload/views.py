
import os

from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status, views
from rest_framework.response import Response

from .models import FileMetadata
from .serializers import FileMetadataSerializer


class UploadFileAPI(views.APIView):
    def post(self, request):
        try:
            file = request.data.get('file')
            name = file.name
            data = {
                "file": file,
                "file_name": name,
                "size" : file.size,
                "file_type" : name.split(".")[1]
            }
            print(data)
            serializer = FileMetadataSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('file_id'), status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(err)
            return Response({"message":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReadUpdateDeleteFileAPI(views.APIView):
    # read file data
    def get(self, request, fileId):
        try:
            file_metadata = get_object_or_404(FileMetadata, pk=fileId)
            return FileResponse(file_metadata.file, as_attachment=True)
        except Exception as err:
            return Response({"message":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # update file data

    def put(self, request, fileId):
        file_metadata = get_object_or_404(FileMetadata, pk=fileId)

        new_file = request.data.get('file')
        if new_file and file_metadata.file:
            old_file_path = file_metadata.file.path
            try:
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)
            except OSError as e:
                return Response({"message": f"Error deleting old file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        file = request.data.get('file')
        name = file.name

        file_metadata.file_name = name
        file_metadata.size = file.size
        file_metadata.file_type = name.split('.')[1]
        serializer = FileMetadataSerializer(file_metadata, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # delete file
    def delete(self, request, fileId):
        try:
            file_metadata = get_object_or_404(FileMetadata, pk=fileId)

            if file_metadata.file:
                file_path = file_metadata.file.path
                file_metadata.file.delete(save=True) 
                # logic depends on where the media is stored, for now i am deleting from my local
                try:
                    os.remove(file_path) 
                except OSError as e:
                    print("Error while deleting file: ", e)
            file_metadata.delete()
            return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response({"message":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListFilesAPI(views.APIView):
    def get(self, request):
        try:
            files = FileMetadata.objects.all()
            serializer = FileMetadataSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"message":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)