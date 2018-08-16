#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : group.py
# @Software: bianbian's PyCharm
# @Time    : 2018/8/13 9:43

import uuid

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

__all__ = ["UserGroup"]


class UserGroup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_("Name"))
    comment = models.TextField(blank=True, verbose_name=_("Comment"))
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Date created"))
    create_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("User group")

    @classmethod
    def initial(cls):
        default_group = cls.objects.filter(name='Default')
        if not default_group:
            group = cls(name='Default', create_by='System', comment=_('Default user group'))
            group.save()
        else:
            group = default_group[0]
        return group

    @classmethod
    def generate_fake(cls, count=100):
        from random import seed, choice
        import forgery_py
        from . import User

        seed()
        for i in range(count):
            group = cls(name=forgery_py.name.full_name(),
                        comment=forgery_py.lorem_ipsum.sentence(),
                        create_by=choice(User.objects.all()).username)
            try:
                group.save()
            except IntegrityError:
                print('Error continue')
                continue
