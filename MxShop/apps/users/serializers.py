# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/10 0010 15:19'

import re
from datetime import datetime
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    验证注册号码
    因为只是验证号码（用户只输入号码），前端不传递code过来（code是自己生成的）。
    如果用ModelSerializer，前端不传递code，code又是必填字段。会报错
    """
    mobile = serializers.CharField(max_length=11)  # 和前端一致名称

    def validate_mobile(self, mobile):
        ''' 手机号码验证方法：必须 validate_ + 字段名'''
        if User.objects.filter(mobile=mobile).count():
            # 如果存在此号码记录，不给注册。让用户直接登录
            raise serializers.ValidationError("已存在此号码，请前往登录")

        if not re.match(REGEX_MOBILE, mobile):
            # 判断号码是否合法。如果号码第一个匹配不正确，则抛出异常
            raise serializers.ValidationError("手机号码非法")

        # 限制发送验证码频率
        # 60秒内只能发送一次
        one_minuter_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)  # 发送验证码前一分钟内
        # 刚刚发送的时间大于刚刚发送时间的一分钟内，（过了前60秒（add_time = one_minuter_age）则不给发送）
        if VerifyCode.objects.filter(add_time__gt=one_minuter_age, mobile=mobile).count():
            # 刚刚发送的时间还在一分钟内（"刚刚发送的时间"大于一分钟内 (刚刚发送时间-60秒)），不给发送（发送验证码）
            raise serializers.ValidationError("60内不得发送")

        return mobile  # 记得方法里面返回结果，不然debug获取不到mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    验证用户的code
    用户传递的code要进行验证，但是不保存到数据库
    """
    # 会在测试显示code错误。不保存到数据库，所以在此新建serializers验证就行.help_text在测试显示中文。required：只能在获取不到code字段才生效
    # error_messages：自定义错误;label：显示为中文
    code = serializers.CharField(label="验证码",required=True, write_only=True, max_length=4, min_length=4,
                                 error_messages={
                                     "blank": "输入不能为空",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"

                                 },
                                 help_text="验证码")
    # 在测试显示username错误。allow_blank 不能为空。queryset查询数据库有没有此用户。（不能注册过的）
    username = serializers.CharField(required=True,allow_blank=False,help_text="用户名",label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(),message="用户已经存在")]
                                     )

    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True
    )

    # def create(self, validated_data):
    #     '''密码加密保存'''
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)  # 创建当前model的对象
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        '''
        如果验证码过期(如果过去five_minuter _age，)；输入错误的验证码；错误格式的验证码；
        :return: 不需要return code，不保存数据库
        '''

        # initial_data['username']：post过来的值。排序取到最近的记录
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        # 验证code
        if verify_records:
            last_records = verify_records[0]  # 取第一个（最新）code
            five_minutes_age = datetime.now() - timedelta(hours=1, minutes=5, seconds=0)
            if five_minutes_age > last_records.add_time:  # 超过5分钟就算超时
                # 发送验证码倒计时5分钟，所以five_minutes_age > add_time后就过去5分钟了（现在时间大于前五分钟，说明已经过去5分钟了）
                raise serializers.ValidationError("验证码超时")  # 验证码过期就不用执行下面代码了
            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("没有此验证码")

    def validate(self, attrs):
        '''
        验证完code，再删除code
        :param attrs: 此UserSerializer的所有方法
        '''
        attrs["mobile"] = attrs["username"]  # 自己把username(手机号码)传递给mobile
        del attrs["code"]  # 删除自定义的code,不需要传递给数据库
        return attrs

    class Meta:
        model = User
        # 用户输入号码传递给username，不是传递给mobile，所以mobile要为空,后端自己把username的"mobile"赋值给models / mobile
        fields = ("username", "code", "mobile", "password")  # 在测试页面显示
