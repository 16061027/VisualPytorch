from django.conf.urls import url
from user import views
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token
from django.urls import include
import social_django

urlpatterns = [
    url(r'^register/$', views.UserRegister.as_view()),
    url(r'^login/$',obtain_jwt_token),
    url('', include('social_django.urls', namespace='social'))
]