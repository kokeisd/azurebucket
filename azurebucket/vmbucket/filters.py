from django_filters import FilterSet

from .models import VMBucket


class VMBucketFilter(FilterSet):
    class Meta:
        model = VMBucket
        #fields = {"host": ["exact", "contains"], "userid": ["exact","contains"]}
        #fields = {"name": ["exact", "contains"]}
        #fields = []
        fields = {"name": ["icontains"], 
                "subscription": ["icontains"]
                }
        exclude = {"id"}
        type='contains'
