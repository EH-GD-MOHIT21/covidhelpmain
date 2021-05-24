from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class userpersonal(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=15)
    email = models.EmailField()
    unicode = models.CharField(max_length=100,null=True)
    timestamp = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)