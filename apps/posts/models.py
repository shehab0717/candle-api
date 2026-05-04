from django.db import models
from django.conf import settings
from common.models import TimestampedModel
from common.utils import UploadTo


class Post(TimestampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=5000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def __str__(self):
        return self.title


class PostAttachment(models.Model):
    file = models.FileField(upload_to=UploadTo("posts/"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachments")
