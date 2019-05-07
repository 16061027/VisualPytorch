from django.shortcuts import render
from journal.models import *
from django.db.models import *
from journal.serializers import *
from NeuralNetwork.models import *
from BaseApiView.views import BaseApiView as APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.


class Visit(APIView):

    def post(self, request):
        count = VisitCount.objects.all()

        # 记录ip访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
            client_ip = client_ip.split(",")[0]
        else:
            client_ip = request.META['REMOTE_ADDR']

        exist = UserIp.objects.filter(ip=str(client_ip))
        if exist:
            uip = exist[0]
            uip.count += 1
        else:
            uip = UserIp()
            uip.ip = client_ip
            uip.count = 1
        uip.save()

        # 增加今日访问次数
        date = timezone.now().date()
        today = DayCount.objects.filter(day=date)
        if today:
            day_record = today[0]
            day_record.count += 1
        else:
            day_record = DayCount()
            day_record.dayTime = date
            day_record.count = 1
        day_record.save()
        return Response(status=status.HTTP_201_CREATED)


class Statistics(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            vist_count = UserIp.objects.aggregate(Sum('count'))
            date_count_list = DayCount.objects.all()
            network_api_count = Network.objects.count()
            date_count_list_serializer = DayCountSerializer(date_count_list, many=True)
        except BaseException:
            return Response({"error": "some error happened"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "visit_count": vist_count['count__sum'],
            "date_count_list": date_count_list_serializer.data,
            "network_api_count": network_api_count,
        }
        return Response(data, status=status.HTTP_200_OK)
