from django.conf.urls import url
from NeuralNetwork import views

urlpatterns = [
    url(r'^network/$', views.NetworkList.as_view()),
    url(r'^getcode/$', views.gen_code),
    url(r'^network/(?P<pk>[0-9]+)/$', views.NetworkDetail.as_view())
]