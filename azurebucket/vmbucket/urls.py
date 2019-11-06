from .views import CreateView
from .views import UpdateView
from .views import ListVMView
from django.conf.urls import url, include

urlpatterns = [
    url(r'^vmbucket/create/$', CreateView.as_view(), name="Create"),
    url(r'^vmbucket/update/(?P<name>.+)/$', UpdateView.as_view(), name="Update"),
    url(r'^vmbucket/$', ListVMView.as_view(), name="List"),

]



