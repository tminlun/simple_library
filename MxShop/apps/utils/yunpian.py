# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/3/10 0010 13:19'

import requests
import json


class YunPian(object):
    """
    通过第三方：云片网发送短信验证码
    api_key：828bb1c73cae18e05c184969679cbd3e

    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self,code,mobile):
        ''' 发送验证码方法 '''
        # 需要传递的参数
        parmas = {
            "apikey": self.api_key,
            "mobile":  mobile,
            "text": "【田敏伦test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)  # 传递parmas给客户端，客户端验证成功返回数据
        print(response.text)
        re_dict = json.loads(response.text)  # 将字符串转换为python类型(字典) 必须转换
        print(re_dict)
        return re_dict


def mian():
    yun_pian = YunPian('828bb1c73cae18e05c184969679cbd3e')
    yun_pian.send_sms('5201314', '15625873905')


if __name__ == '__main__':
    mian()

