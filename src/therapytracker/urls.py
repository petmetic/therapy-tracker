from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r"su/", include("django_su.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
]
