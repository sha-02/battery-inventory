from django.test import TestCase

# Create your tests here.

# https://python.doctor/page-django-query-set-queryset-manager
from battery.models import Device

# _test = Device.objects.filter(user=request.user, description='jdoe Dev2').values()
res = Device.objects.filter(description='jdoe Dev2')
res
res.values()