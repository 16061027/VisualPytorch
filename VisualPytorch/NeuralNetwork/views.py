from django.shortcuts import render
from django.shortcuts import render_to_response
from NeuralNetwork.models import Network
from NeuralNetwork.serializers import NetworkSerializer
from NeuralNetwork.permissions import ChangeModel
from BaseApiView.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .translate import ops
from rest_framework import permissions
import os
from django.conf import settings
from django.http import FileResponse
import json
from django.db.models import Q


# Create your views here.

class NetworkList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_id = request.GET['id']
        if user_id is None:
            return Response("need user id", status=status.HTTP_400_NOT_FOUND)
        network_list = Network.objects.filter(creator=user_id).values('id', 'time', 'creator_id', 'name')
        return Response(list(network_list), status=status.HTTP_200_OK)

    def post(self, request):

        creator = request.user.id
        data = {
            "name": request.data["name"],
            "creator": creator,
            "structure": json.dumps(request.data["structure"])
        }
        serializer = NetworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NetworkDetail(APIView):
    permission_classes = (ChangeModel,)


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
        data = {
            "name": request.data["name"],
            "structure": json.dumps(request.data["structure"])
        }
        serializer = NetworkSerializer(net, data=data)
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
    except Exception as e:
        return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(result, status=status.HTTP_200_OK)


# todo:这里仅仅是简单的样例
def download_project(request):
    file = open(os.path.join(settings.FILE_DIR, "test.jpg"), "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="rika_suki.jpg"'
    return response
