from django.contrib import admin
from django.conf.urls import include, url
from parts_api import views

urlpatterns = [
    url("home/", views.home, name="home"),
    url("admin/", admin.site.urls),
    url(r"part/(?P<part_id>\w+)", views.update_part, name="update_part"),
    url("part/", include("drf_part.urls")),
    url("nltk/", include("drf_nltk.urls")),
]
