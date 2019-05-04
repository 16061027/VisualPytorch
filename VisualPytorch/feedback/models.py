from django.db import models


# Create your models here.
class FeedBack(models.Model):
    title = models.CharField(max_length=32, default='Title')
    content = models.TextField(null=True)
