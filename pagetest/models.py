from __future__ import unicode_literals

from django.db import models


# Create your models here.

class SomeData(models.Model):
    data_int = models.IntegerField(default=0)
    data_string = models.CharField(max_length=20, default='')
