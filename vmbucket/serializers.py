from rest_framework import serializers
from .models import VMBucket

class VMBucketSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = VMBucket
        #fields = ('subscription', 'resource_group', 'name', 'primary_ip', 'location', 'vm_size','os_disk', 
         #           'os_disk_size', 'status', 'disks', 'avset', 'tags', 'created_time')
        fields = '__all__'
        #read_only_fields = ('created_time')
