# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/1 0001 17:12'
"""
测试，django和drf作比较
"""

from django.views.generic.base import View
from django.views.generic import ListView
from .models import Goods


class GoodsListView(View):
    """
    商品列表。通过json把全部数据传递给前端，因为是多个数据所以要添加到list
    all 、filter都要进行遍历
    注：没有提示说明有错误
    """
    def get(self,request):
        # 所有json数据添加到列表
        json_list = []

        goods = Goods.objects.all()[:10]
        # 把数据通过json传递给前端

        # json_desc = {}
        #         # for good in goods:
        #         #     json_desc['name'] = good.name
        #         #     json_desc['category'] = good.category.name
        #         #     json_desc['market_price'] = good.market_price
        #         #     json_list.append(json_desc)

        # for good in goods:
        #     from django.forms.models import model_to_dict  # 把models对象转换为dict对象
        #     json_desc = model_to_dict(good)
        #     json_list.append(json_desc)
        from django.core import serializers
        import json
        json_desc = serializers.serialize("json", goods)  # 字符串
        # json.loads(json_desc)  # 将字符串转换成 python对象

        from django.http import JsonResponse
        import json

        # json.dumps：将json_list的 Python 对象(desc、list)编码成字符串
        return JsonResponse(json.loads(json_desc),safe=False)
