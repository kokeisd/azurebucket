from .views import CreateView
from .views import DetailsView
from .views import ListVMView
from django.conf.urls import url, include

urlpatterns = [
    url(r'^vmbucket/create/$', CreateView.as_view(), name="Create"),
    url(r'^vmbucket/$', ListVMView.as_view(), name="List"),
]


