import django_tables2 as tables
from .models import VMBucket

class VMBucketTable(tables.Table):
   # host = tables.Column(linkify=True)
   # id = tables.Column(linkify=True)

    class Meta:
        model = VMBucket
        template_name = "django_tables2/bootstrap.html"
