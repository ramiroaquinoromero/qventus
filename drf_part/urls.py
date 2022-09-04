from django.conf.urls import url
from drf_part import views

urlpatterns = [
    url('', views.part_rest_list, name='part_rest_list')
]
