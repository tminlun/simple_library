from rest_framework.views import APIView  # 和View功能一样，是View的进阶版
from goods.serializers import GoodsSerializer  # 和Django的forms、modelsforms功能一样
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from .models import Goods

# Create your views here.


class GoodsPagination(PageNumberPagination):
    '''
    自定义分页（可以注释全局的分页了）
    '''
    # 默认每页显示的个数
    page_size = 10
    # 让前端（用户）可以手动 动态改变每页显示的个数：&page_size=?
    page_size_query_param = 'page_size'
    # 页码的参数（url的参数page=?）
    page_query_param = 'page'
    # 最多能显示100页
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, GenericViewSet):
    '''
    商品列表,这里可以在drf显示哦
    '''
    pagination_class = GoodsPagination
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer



