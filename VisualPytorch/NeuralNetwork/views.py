from django.shortcuts import render
from django.shortcuts import render_to_response
from NeuralNetwork.models import Network
from NeuralNetwork.serializers import NetworkSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .translate import ops


# Create your views here.

class NetworkList(APIView):

    def get(self, request):
        networklist = Network.objects.all()
        serializer = NetworkSerializer(networklist, many=True)
        return Response(serializer.data)

    def post(self, request):

        data = {
            "creator": -1,
            "structure": str(request.data)
        }

        serializer = NetworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NetworkDetail(APIView):

    def get_object(self, pk):
        try:
            return Network.objects.get(pk=pk)
        except Network.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        net = self.get_object(pk)
        serializer = NetworkSerializer(net)
        return Response(serializer.data)

    def put(self, request, pk):
        net = self.get_object(pk)
        serializer = NetworkSerializer(net, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        net = self.get_object(pk)
        net.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def gen_code(request):
    result = {}
    try:
        result["Main"], result["Model"], result["Ops"] = ops.main_func(request.data)
    except BaseException:
        return Response({"error": "some error happened"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(result, status=status.HTTP_200_OK)
