from django.db import models

# Create your models here.

class publicaccessdata(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=20)
    first_contact = models.CharField(max_length=13)
    second_contact = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    facilities = models.TextField()
    desc = models.TextField()
    verified = models.BooleanField(default=False)