from .views import CreateView
from .views import DetailsView
from django.conf.urls import url, include

urlpatterns = [
    url(r'^vmbucket/create/$', CreateView.as_view(), name="create"),
    url(r'^vmbucket/$', DetailsView.as_view(), name="Details"),
]

