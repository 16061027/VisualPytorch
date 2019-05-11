from django.conf.urls import url
from journal import views

urlpatterns = [
    url('visit/', views.Visit.as_view()),
    url('statistics/', views.Statistics.as_view())

]