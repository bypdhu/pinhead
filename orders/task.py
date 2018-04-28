#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : task.py
# @Software: bianbian's PyCharm
# @Time    : 2018/1/3 18:01

from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    """
    task to send an e-mail notification when an order is successfully created.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.' \
              'Your order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'bianbian<bianbian@ehousechina.com>', [order.email])
    return mail_sent