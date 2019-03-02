# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/1 0001 19:49'

from rest_framework import serializers

from goods.models import Goods,GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    """
    所有的GoodsCategory字段
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    """
    所有的Goods字段
    """
    # 同modelforms，可以添加字段（也可以实例化CategorySerializer的category）来覆盖默认的字段（Goods的category）
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'
