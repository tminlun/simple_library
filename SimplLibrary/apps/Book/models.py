from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=50,verbose_name="名字")
    publish = models.CharField(max_length=32,verbose_name="发表",blank=True)
    author = models.CharField(max_length=32,verbose_name="作者")
    price = models.IntegerField(default=0,verbose_name="价格")
    add_time = models.DateTimeField(default=datetime.now,verbose_name='时间')

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
