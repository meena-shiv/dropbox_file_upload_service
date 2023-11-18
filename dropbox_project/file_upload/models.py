import uuid

from django.db import models

# Create your models here.

class FileMetadata(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField()
    file_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.file_name