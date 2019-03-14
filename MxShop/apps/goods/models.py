from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类别"),
        (2, "二级类别"),
        (3, "三级类别")
    )
    name = models.CharField(default="",max_length=30,verbose_name="类别名",help_text="类别名")
    code = models.CharField(default="",max_length=30,verbose_name="类别英文名",help_text="类别英文名")
    desc = models.TextField(default="",verbose_name="类别的描述",help_text="类别的描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE,default=1,verbose_name="类别级别",help_text="类别级别")
    # 当前类别的父类别，一级类别不需要父类别，所以要为空。可以通过当前类别反向查询所有的子类别
    parent_category = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,verbose_name="当前类别的父级",related_name="sub_cat",help_text="当前类别的父级")
    is_banner = models.BooleanField(default=False,verbose_name="是否为轮播类别",help_text="是否为轮播类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间",help_text="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    商品类别的（广告）品牌图片
    """
    category = models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,null=True,blank=True,verbose_name="类别")
    name = models.CharField(default="", max_length=30, verbose_name="广告对应的类别", help_text="品牌名")
    # imagefield在数据库为char，所以max_length
    image = models.ImageField(max_length=200,upload_to="brands",verbose_name="品牌的图片", help_text="品牌的图片")
    desc = models.TextField(default="", verbose_name="品牌的介绍", help_text="品牌的介绍")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间",help_text="添加时间")

    class Meta:
        verbose_name = "类别广告的图片和介绍"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目")
    goods_sn = models.CharField("商品唯一货号", max_length=50, default="")
    name = models.CharField("商品名", max_length=100)
    click_num = models.IntegerField("点击数", default=0)
    sold_num = models.IntegerField("商品销售量", default=0)
    fav_num = models.IntegerField("收藏数", default=0)
    goods_num = models.IntegerField("库存数", default=0)
    market_price = models.FloatField("市场价格", default=0)
    shop_price = models.FloatField("本店价格", default=0)
    goods_brief = models.TextField("商品简短描述", max_length=300)
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    ship_free = models.BooleanField("是否承担运费", default=True)
    # 首页中展示的商品封面图
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    # 首页中新品展示
    is_new = models.BooleanField("是否新品", default=False)
    # 商品详情页的热卖商品，自行设置
    is_hot = models.BooleanField("是否热销", default=False)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    def goods_descs(self):
        ''' 限制内容的长度 '''
        if len(str(self.goods_desc)) > 65:
            return '{}...'.format(str(self.goods_desc)[:65])
        else:
            return str(self.goods_desc)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品图片（1（食物）对 多（图片）），就要用外键
    """
    # related_name：通过related_name把所有对应图片传递给goods
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name="goods_banner",verbose_name="商品")
    image = models.ImageField(upload_to="goods/images/",max_length=200,null=True,blank=True,verbose_name="图片")
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsBanner(models.Model):
    """
    大图：首页的goods轮播图（首页轮播图如果使用goodsimage会拉伸的很难看，所以需要再定义一个）
    """
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="商品")
    image = models.ImageField(max_length=200,upload_to="brands/",verbose_name="轮播图片")
    index = models.IntegerField(default=0,verbose_name="轮播顺序")  # order_by进行排序
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = 'goods首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
