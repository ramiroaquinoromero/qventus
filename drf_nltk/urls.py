from django.conf.urls import url
from drf_nltk import views

urlpatterns = [
    url('', views.part_common_word_list, name='part_common_word_list')
]
