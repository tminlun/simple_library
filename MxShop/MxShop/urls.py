"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import xadmin
from django.urls import path, include, re_path
from django.conf import settings #上传图片
from django.conf.urls.static import static #上传图片
from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()  # 自动添加get、post、patch方法
# 配置goods的url
router.register('goods', GoodsListViewSet)


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # api显示登录按钮
    path('api-auth/', include('rest_framework.urls')),
    path('docs',include_docs_urls(title='慕课网生鲜超市')),
    # 富文本编辑器url
    path('ueditor/',include('DjangoUeditor.urls')),

    # 商品列表页
    re_path('^', include(router.urls)),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)