# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/1 0001 19:49'

from rest_framework import serializers

from goods.models import Goods,GoodsCategory,GoodsImage


class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    三级分类
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    二级分类
    """
    # 通过二级分类反向查询第三级分类（GoodsCategory.sub_cat.sub_cat）
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    一级分类：
        many=True：列表必须加
    """
    # 反向查询第二级分类（GoodsCategory.sub_cat）,同时还把一二三级分类全部系列化出来
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    '''获取商品轮播图：goods的外键'''
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    """
    系列化Goods列表
    """
    # 同ModelForms，可以添加字段（也可以实例化CategorySerializer的category）来覆盖默认的字段（Goods的category）
    category = GoodsCategorySerializer()
    goods_banner = GoodsImageSerializer(many=True)  # goods通过related_name,反向查询所有的轮播图（Goods.goods_banner）

    class Meta:
        model = Goods
        fields = '__all__'
