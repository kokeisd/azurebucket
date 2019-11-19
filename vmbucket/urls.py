from .views import CreateView
from .views import UpdateView
from .views import ListAllVMView
from .views import ListVMView
from .views import ListVMWebView
from django.conf.urls import url, include


urlpatterns = [
    #url(r'^vmbucket/web/list/$', ListVMWebView.as_view()),
    #url(r'^vmbucket/create/$', CreateView.as_view(), name="Create"),
    #url(r'^vmbucket/(?P<name>.+)/update/$', UpdateView.as_view(), name="Update"),
    #url(r'^vmbucket/(?P<name>.+)/delete/$', UpdateView.as_view(), name="Delete"),
    #url(r'^vmbucket/(?P<name>.+)/$', ListVMView.as_view(), name="List VM details"),
    #url(r'^vmbucket/$', ListAllVMView.as_view(), name="List All VM details"),

    url(r'^vmbucket/web/list/$', ListVMWebView.as_view()),
    url(r'^vmbucket/create/$', CreateView.as_view(), name="Create"),
    url(r'^vmbucket/update/(?P<name>.+)/$', UpdateView.as_view(), name="Update"),
    url(r'^vmbucket/read/(?P<name>.+)/$', ListVMView.as_view(), name="List VM details"),
    url(r'^vmbucket/list/', ListAllVMView.as_view(), name="List All VM details"),

]




