from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_public=models.BooleanField(default=False)

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.CharField(max_length=300,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    end_at=models.DateTimeField()

    def __str__(self):
        return self.user.username