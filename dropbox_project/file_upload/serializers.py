from rest_framework import serializers

from .models import FileMetadata


class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = ['file_id', 'file_name', 'created_at', 'size', 'file_type', 'file']
        