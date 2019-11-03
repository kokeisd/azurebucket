from django.shortcuts import render
from .models import VMBucket
from .serializers import VMBucketSerializer
from rest_framework import generics

# Create your views here.


class CreateView(generics.ListCreateAPIView):
   # logger = logging.getLogger(__name__)
    """This class defines the create behavior of our rest api."""
    queryset = VMBucket.objects.all()
    serializer_class = VMBucketSerializer
    #logger.debug('CreateView***********')
    def perform_create(self, serializer):
        serializer.save()