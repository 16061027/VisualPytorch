from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^register/$', views.UserRegister.as_view()),
]