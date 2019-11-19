from django_filters import FilterSet

from .models import VMBucket


class VMBucketFilter(FilterSet):
    class Meta:
        model = VMBucket
        #fields = {"host": ["exact", "contains"], "userid": ["exact","contains"]}
        #fields = {"name": ["exact", "contains"]}
        #fields = []
        fields = {
                "subscription": ["icontains"],
                "resource_group": ["icontains"], 
                "name": ["icontains"],
                "status": ["icontains"],
                "primary_ip_address": ["icontains"],
                "secondary_ip_addresses": ["icontains"],
                "location": ["icontains"],
                "vm_size": ["icontains"],
                "os_disk": ["icontains"],
                "os_disk_size": ["icontains"],
                "disks": ["icontains"],
                "avset": ["icontains"],
                "tags": ["icontains"],
                "last_update_time": ["icontains"],
                

                }
        exclude = {"id"}
        type='contains'
