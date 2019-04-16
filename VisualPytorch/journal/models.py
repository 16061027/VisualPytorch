from django.db import models
from django.utils import timezone


# Create your models here.

# 访问ip及其对应的访问次数
class UserIp(models.Model):
    ip = models.CharField(max_length=30)
    count = models.IntegerField(default=0)


class VisitCount(models.Model):
    count = models.IntegerField(default=0)


class DayCount(models.Model):
    day = models.DateField(default=timezone.now)
    count = models.IntegerField(default=0)
