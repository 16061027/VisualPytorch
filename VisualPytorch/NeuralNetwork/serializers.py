from rest_framework import serializers
from NeuralNetwork.models import Network

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('id','creator','structure','name','time')
