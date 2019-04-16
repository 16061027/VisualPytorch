from django.conf.urls import url
from journal import views

urlpatterns = [
    url('', views.Visit.as_view()),
]