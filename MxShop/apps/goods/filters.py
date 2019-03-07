# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/3 0003 23:17'

from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """ 商品过滤类 """
    # Goods.objects.filter(shop_price__gt=)：显示所有大于等于shop_prices的值
    pricemin = filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # method：能够过滤自己定义的函数.category：goods的外键分类
    top_category = filters.NumberFilter(field_name="category", method="top_category_filter")

    def top_category_filter(self, queryset, name, value):
        ''' 能够过滤自己定义的函数；queryset,name,value：默认参数；value：传递过来的'category_id'''
        # 如果是三级分类，或者二级分类可以通过parent_category进行筛选所有的父类；不管点击一级、二级、三级分类都可以找到
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))  # 筛选对应的分类ID（value）,返回给分类列表

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']
