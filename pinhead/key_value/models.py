# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class KeyValue(models.Model):
    key = models.CharField(max_length=128)
    display_name = models.CharField(max_length=256, blank=True)
    type_list = (
        ('string', '字符串'),
        ('number', '数字'),
        ('list', '列表'),
        ('json', 'json'),
        ('datetime', '日期时间'),
        
    )
    value_type = models.CharField(max_length=16, choices=type_list, default='string') 
    value = models.CharField(max_length=256, blank=True)
    
    
class Value(models.Model):
    boolean_value = models.BooleanField(default=True)
    char_value = models.CharField(max_length=32)
    email_value = models.EmailField()
    file_value = models.FileField(upload_to='key_value/')
    
    datetime_create_value = models.DateTimeField(auto_now_add=True)
    datetime_update_value = models.DateTimeField(auto_now=True)
