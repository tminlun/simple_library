# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/2/27 0027 13:19'

#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence 
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from .models import GoodsFav, UserLeavingMessage, UserAddress


class GoodsFavAdmin(object):
    list_display = ['user', 'goods', "add_time"]


class UserLeavingMessageAdmin(object):
    list_display = ['user','subject', 'message_type', "message", "add_time"]


class UserAddressAdmin(object):
    list_display = ["signer_name", "signer_moblie", "district", "address"]


xadmin.site.register(GoodsFav, GoodsFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)