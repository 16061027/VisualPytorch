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
import zipfile
from django.conf import settings
from django.http import FileResponse,StreamingHttpResponse
import json
import shutil
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


#todo:虽然看起来没啥问题但是问题绝对很大
@api_view(['POST'])
def download_project(request):

    if os.path.exists(os.path.join(settings.FILE_DIR,"project")):
        shutil.rmtree(os.path.join(settings.FILE_DIR,"project"))
    if os.path.exists("project_VisualPytorch.zip"):
        os.remove("project_VisualPytorch.zip")
    data = request.data
    root_dir = os.path.join(settings.FILE_DIR,"project")
    os.mkdir(root_dir)
    file_main = open(os.path.join(root_dir, "Main.py"), "w")
    file_model = open(os.path.join(root_dir, "Model.py"), "w")
    file_ops = open(os.path.join(root_dir, "Ops.py"), "w")

    file_main.write(data['main'])
    file_model.write(data['model'])
    file_ops.write(data['ops'])

    zipf = zipfile.ZipFile("project_VisualPytorch.zip", 'w',zipfile.ZIP_DEFLATED)
    pre_len = len(settings.FILE_DIR)
    for parent, dirnames, filenames in os.walk(settings.FILE_DIR):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    response = StreamingHttpResponse(file_iterator("project_VisualPytorch.zip"))
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = 'attachment;filename="project_VisualPytorch.zip"'
    return response


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

