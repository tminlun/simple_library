from datetime import datetime
from django.db import models
from users.models import UserProfile
from goods.models import Goods

# Create your models here.


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="购物车商品")
    goods_nums = models.IntegerField(default=0,verbose_name="商品的数量")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.goods,self.goods_nums)


class OrderInfo(models.Model):
    """
    商品订单信息
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )
    PAY_TYPE = (
        ("alipay", "支付宝"),
        ("wechat", "微信"),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    # unique=True：订单号唯一
    order_sn = models.CharField("订单编号", max_length=30, null=True, blank=True, unique=True)
    # 微信支付会用到
    nonce_str = models.CharField("微信支付随机加密串", max_length=50, null=True, blank=True, unique=True)
    # 支付宝交易号
    trade_no = models.CharField("支付宝交易号", max_length=100, unique=True, null=True, blank=True)
    # 支付状态
    pay_status = models.CharField("订单状态", choices=ORDER_STATUS, default="paying", max_length=30)
    # 订单的支付类型
    pay_type = models.CharField("支付类型", choices=PAY_TYPE, default="alipay", max_length=10)
    post_script = models.CharField("订单留言", max_length=200)
    order_mount = models.FloatField("订单金额", default=0.0)
    pay_time = models.DateTimeField("支付时间", null=True, blank=True)

    # 用户信息
    address = models.CharField("收货地址", max_length=100, default="")
    signer_name = models.CharField("签收人", max_length=20, default="")
    singer_mobile = models.CharField("联系电话", max_length=11)

    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    商品的订单、商品数量
    """
    # 一个订单对应多个商品
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE,verbose_name="订单",related_name="goods")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="订单的商品")
    goods_nums = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "商品订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)