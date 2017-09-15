from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    nickname = models.CharField(max_length=64)
    user = models.OneToOneField(User)