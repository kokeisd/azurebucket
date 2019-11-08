from django.shortcuts import render
from .models import VMBucket
from .serializers import VMBucketSerializer
from rest_framework import generics
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from .filters import VMBucketFilter
from .tables import VMBucketTable

# Create your views here.


class CreateView(generics.ListCreateAPIView):
   # logger = logging.getLogger(__name__)
    """This class defines the create behavior of our rest api."""
    queryset = VMBucket.objects.all()
    serializer_class = VMBucketSerializer
    #logger.debug('CreateView***********')
    def perform_create(self, serializer):
        serializer.save()

class ListVMView(generics.ListAPIView):
  serializer_class = VMBucketSerializer

  def get_queryset(self):
     #hostname = self.request.hostname
     hostname = self.kwargs['name']
#data = {"results": list(details.values('id', 'name','host','cmd','output', 'date_created', 'date_modified'))}
     return VMBucket.objects.filter(name=hostname)
  

class ListAllVMView(generics.ListAPIView):
  serializer_class = VMBucketSerializer

  def get_queryset(self):
     #hostname = self.request.hostname     
     return VMBucket.objects.filter()

class UpdateView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
  #  logger = logging.getLogger(__name__)
  #  logger.debug('CreateView***********')
    queryset = VMBucket.objects.all()
    serializer_class = VMBucketSerializer
    lookup_url_kwarg = 'name'
    lookup_field = 'name'

class ListVMWebView(ExportMixin, SingleTableMixin, FilterView):
    table_class = VMBucketTable
    model = VMBucket
    template_name = "listvm.html"
    filterset_class = VMBucketFilter
    export_formats = ("csv", "xls")

  #  def get_queryset(self):
      #return super().get_queryset().select_related("host")
    
    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}