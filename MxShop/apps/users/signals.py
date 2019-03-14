# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/13 0013 19:35'

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


# 保存最后一刻，加密注册密码
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    '''
    在Model调用save/delete方法进行保存的最后时刻，要做一些定制的行为： post_save
    :param sender:模型类
    :param instance:保存的实际实例（对象）
    :param created:True表示已经创建了新记录,False:暂未创建新记录
    '''
    if created:
        password = instance.password  # #instance相当于user
        instance.set_password(password)  # 加密
        instance.save()
