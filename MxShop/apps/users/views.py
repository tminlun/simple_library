from random import choice
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin  # 实例化
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from MxShop.settings import APIKEY
from utils.yunpian import YunPian

from .serializers import SmsSerializer,UserRegSerializer
from .models import VerifyCode

User = get_user_model()
# Create your views here.


class CustomBackend(ModelBackend):
    """
    重载authentication，用户名和手机号码登录都可以登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                # 如果有此密码
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    CreateModelMixin：获取post的数据，存储到数据库
    """
    serializer_class = SmsSerializer  # 实例化表单

    def generate_code(self):
        ''' 获取4个随机验证码 '''
        seeds = "1234567890"
        code_str = []
        for i in range(4):
            code_str.append(choice(seeds))  # choice随机在seeds取出一个数字
        return "".join(code_str)  # "".join：""分割数字，返回字符串

    def create(self, request, *args, **kwargs):
        '''
        重写CreateModelMixin方法
        逻辑：
            获取serializer，判断serializer是否合法，合法获取mobile，
            发送验证码，判断是否发送成功，发送成功 手机号码验证码保存到数据库
         '''
        # 获取serializer，判断serializer是否合法（不用修改）
        serializer = self.get_serializer(data=request.data)  # 获取serializer_class
        serializer.is_valid(raise_exception=True)  # 判断输入是否合法（forms的is_valid），不合法，不执行以下代码
        # 如果是合法，获取mobile,code
        mobile = serializer.validated_data["mobile"]
        code = self.generate_code()

        # 发送验证码
        yun_pian = YunPian(APIKEY)
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        # 判断是否发送成功（code == 0则发送成功）
        if sms_status['code'] != 0:
            # 发送失败
            return Response({
                "mobile": sms_status['msg'],  # sms_status['msg']：传递serializer自带的错误
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 发送成功
            # 保存号码和验证码到数据库
            verify_code = VerifyCode(code=code,mobile=mobile)
            verify_code.save()
            return Response({
                "mobile": mobile,  # 号码发送给前端
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''
    用户注册 需要保存数据库：CreateModelMixin
    '''
    serializer_class = UserRegSerializer  # 系列化serializer
    queryset = User.objects.all()  # queryset：保存到User模型(对User进行实现CreateModelMixin)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # 获取serializer
        serializer.is_valid(raise_exception=True)  # 验证
        user = self.perform_create(serializer)  # 获取serializer的model
        re_dict = serializer.data  # 将系列化后的数据，传递给re_dict（客户端）
        # 获取token
        payload = jwt_payload_handler(user)  # 传递user参数，得到payload
        re_dict['token'] = jwt_encode_handler(payload)  # 传递payload参数，得到token
        # name 传递给前端
        re_dict['name'] = user.name if user.name else user.username  # username

        headers = self.get_success_headers(serializer.data)
        # serializer.data 保存了序列化后的数据
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        '''获取对象：UserRegSerializer的model（User）'''
        serializer.save()
