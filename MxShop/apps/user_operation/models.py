from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()
# Create your models here.


class GoodsFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品",help_text="商品id")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = '商品收藏'
        verbose_name_plural = verbose_name
        # 设置user不能有同一时间收藏同个goods
        unique_together = ("user", "goods")

    def __str__(self):
        return "{0}收藏{1}".format(self.user.username,self.goods)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    province = models.CharField(max_length=10,default="",verbose_name="省份")
    city = models.CharField(max_length=10,default="",verbose_name="城市")
    district = models.CharField(max_length=100,default="",verbose_name="区域")
    address = models.CharField(max_length=200,default="",verbose_name="详细地址")
    signer_name = models.CharField(max_length=30,default="",verbose_name="收货人姓名")
    signer_moblie = models.CharField(max_length=11,default="",verbose_name="收货人手机")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = '添加收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessage(models.Model):
    MESSAGE_CHOICES = (
        (1,"留言"),
        (2,"投诉"),
        (3, "咨询"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_type = models.CharField(max_length=30,choices=MESSAGE_CHOICES,default=1,verbose_name="留言类型")
    subject = models.CharField(max_length=100,default="",verbose_name="主题")
    message = models.TextField(default="",verbose_name="留言内容",help_text="留言内容")
    file = models.FileField(upload_to="message/file/",null=True,blank=True,verbose_name="文件")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject
