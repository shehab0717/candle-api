from django.db import models
from django.contrib.auth.models import AbstractUser
from common.utils import UploadTo


class User(AbstractUser):
    img = models.ImageField(upload_to=UploadTo("user/"), blank=True, null=True)
