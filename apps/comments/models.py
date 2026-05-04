from django.db import models
from django.conf import settings
from apps.posts.models import Post
from common.models import TimestampedModel
from django.core.validators import MinLengthValidator


class PostComment(TimestampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(
        max_length=1000,
        validators=[MinLengthValidator(1, "Comment content cannot be empty")],
    )
