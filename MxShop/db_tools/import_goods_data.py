# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/2/27 0027 20:38'


# 导入goods的数据
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')

import django
django.setup()

from db_tools.data.product_data import row_data
from goods.models import Goods,GoodsCategory,GoodsImage

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    # replace("￥", "")把￥替换成 ""
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))

    # 如果内容不为None传递给goods_brief ,否则: else(为None) 把None转换为""，传递给goods_brief
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    # 取第一张作为封面图  [如果有就传递值，如果没有（else）传递""。image在数据库默认为str ]
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    #取最后一个
    category_name = goods_detail["categorys"][-1]
    # 选用filter不用get。因为filter没有匹配的返回空字符串，不会抛异常，get会抛异常（只能传外键给goods.category,直接传str会出错）
    category = GoodsCategory.objects.filter(name=category_name)
    print(category[0])
    if category:
        goods.category = category[0]  # category是一个对象，goods.category需要字符串，category[0]返回对象的字符串
    goods.save()

    # 商品的图片
    for good_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = good_image
        goods_image_instance.goods = goods # 上面有遍历每一个goods
        goods_image_instance.save()