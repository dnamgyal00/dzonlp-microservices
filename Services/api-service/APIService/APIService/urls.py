
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # The line `path("", include(("base.url"), "base"))` in the URL configuration for the APIService
    # project is including another URL configuration from the "base" app into the main URL
    # configuration.
    path("", include(("base.urls", "base"), "base"))
]
