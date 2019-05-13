from django.db import models


# Create your models here.



class Network(models.Model):

    creator = models.ForeignKey('user.User',on_delete=models.CASCADE,null=True)
    structure = models.TextField()
    name = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)




