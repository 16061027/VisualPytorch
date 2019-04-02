from django.shortcuts import render
from NeuralNetwork.models import Network
from NeuralNetwork.serializers import NetworkSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class NetworkList(APIView):

    def get(self,request):
        networklist = Network.objects.all()
        serializer = NetworkSerializer(networklist,many=True)
        return Response(serializer.data)

    def post(self,request):

        serializer = NetworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class NetworkDetail(APIView):

    def get_object(self, pk):
        try:
            return Network.objects.get(pk=pk)
        except Network.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        net = self.get_object(pk)
        serializer = NetworkSerializer(net)
        return Response(serializer.data)

    def put(self, request, pk):
        net = self.get_object(pk)
        serializer = NetworkSerializer(net,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        net = self.get_object(pk)
        net.delete()
        return Response(status=status.HTTP_200_OK)

