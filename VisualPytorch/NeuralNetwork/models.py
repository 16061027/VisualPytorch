from django.db import models

# Create your models here.

class Network(models.Model):

    creator = models.IntegerField(default=-1)
    structure = models.TextField()
    time = models.DateTimeField()


