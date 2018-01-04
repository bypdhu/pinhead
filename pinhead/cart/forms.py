#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : forms.py
# @Software: bianbian's PyCharm
# @Time    : 2018/1/2 14:39

from django import forms

PRODOCT_QUANTITY_CHOIDCES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODOCT_QUANTITY_CHOIDCES,
        coerce=int
    )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
