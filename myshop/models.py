# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# 一对多的关系：一个产品可以属于一个分类，一个分类可以包含多个产品。
# 
# Category 商品的分类。 包括名字和slug
#
# Product 商品。 包括名字、分类、slug、图片、描述、价格、是否生效（可购买）、创建时间、更新时间


class Category(models.Model):
    name = models.CharField(max_length=127, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=127, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='myshop/products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'), )
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
