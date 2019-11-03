from .views import CreateView
from django.conf.urls import url, include

urlpatterns = [
    url(r'^vmbucket/create/$', CreateView.as_view(), name="create"),
]
