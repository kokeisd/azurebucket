from django.db import models

# Create your models here.

class VMBucket(models.Model):
    subscription = models.CharField(max_length=128,blank=True,null=True)
    resource_group = models.CharField(max_length=128,blank=True,null=True )
    name = models.CharField(max_length=128,blank=False)
    primary_ip_address = models.CharField(max_length=256,blank=True,null=True)
    secondary_ip_addresses = models.CharField(max_length=128,blank=True,null=True)
    location = models.CharField(max_length=128,blank=True,null=True)
    vm_size = models.CharField(max_length=128,blank=True,null=True)
    os_disk = models.CharField(max_length=128,blank=True,null=True)
    os_disk_size = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=128,blank=True,null=True)
    disks = models.CharField(max_length=1024,blank=True,null=True)
    avset = models.CharField(max_length=128,blank=True,null=True)
    tags = models.CharField(max_length=1024,blank=True,null=True)
    last_update_time = models.DateTimeField(auto_now=True,editable=False)



