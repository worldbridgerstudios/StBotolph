from django.contrib import admin
from django.urls import include, path
from election_results.api.urls import urlpatterns as api_urls
from election_results.views import IndexView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("", IndexView.as_view()),
]
