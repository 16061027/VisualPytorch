from rest_framework import serializers
from journal.models import *

class UserIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIp
        fields = ('id','ip','count')

class VisitCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitCount
        fields = ('id','count')


class DayCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayCount
        fields = ('id','day','count')