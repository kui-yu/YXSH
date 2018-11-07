from django.db import models

# Create your models here.
class BaseModel(models.Model):
    img = models.CharField(max_length=300)
    name = models.CharField(max_length=50)
    trackid = models.CharField(max_length=20)
    class Meta:
        abstract = True


class Axf_wheel(BaseModel):

    class Meta:
        db_table = 'axf_wheel'


class Axf_nav(BaseModel):

    class Meta:
        db_table = 'axf_nav'


class Axf_mustBuy(BaseModel):

    class Meta:
        db_table = 'axf_mustbuy'


class Axf_shop(BaseModel):

    class Meta:
        db_table = 'axf_shop'



class Axf_mainshow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=200)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=10)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=8)
    marketprice1 = models.CharField(max_length=8)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2= models.CharField(max_length=100)
    price2 = models.CharField(max_length=8)
    marketprice2 = models.CharField(max_length=8)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=8)
    marketprice3 = models.CharField(max_length=8)

    class Meta:
        db_table = 'axf_mainshow'

#       insert into axf_foodtypes(typeid,typename,childtypenames,typesort)
# values("104749","热销榜","全部分类:0",1)
class Axf_foodtypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_foodtypes'


# insert into axf_goods(productid,productimg,productname,
# productlongname,isxf,pmdesc,specifics,price,marketprice,
# categoryid,childcid,childcidname,dealerid,storenums,productnum)
class Axf_goods(models.Model):
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=0)
    pmdesc =  models.IntegerField(default=0)
    specifics = models.CharField(max_length=20)
    price = models.FloatField(default=0.0)
    marketprice = models.FloatField(default=0.0)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=100)
    dealerid= models.CharField(max_length=16)
    storenums =  models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_goods"

#         用户表
class UserModel(models.Model):
    u_name = models.CharField(max_length=20,unique=True)
    u_password = models.CharField(max_length=32,null=False)
    u_email = models.CharField(max_length=32,unique=True)
    u_sex = models.BooleanField(default=1)
    u_img = models.ImageField(upload_to="img")
    class Meta:
        db_table = 'axf_user'

#    购物车表
# 属性： 1.商品id   2.商品数量  3.是否选中  4.用户id
# 商品 与 用户为多对多

class GoodsCart(models.Model):
    c_goods = models.ForeignKey(Axf_goods)
    c_num = models.IntegerField(default=1)
    c_isselect = models.BooleanField(default=1)
    c_user = models.ForeignKey(UserModel)
    class Meta:
        db_table = 'axf_cart'



class OrderList(models.Model):
    # 订单号,商品id,用户id,创建时间,订单状态
    # 商品用户关系表
    o_Number = models.CharField(max_length=128)
    o_user = models.ForeignKey(UserModel)
    o_status = models.IntegerField(default=1)
    o_createTime = models.DateField(auto_now=True)
    class Meta:
        db_table = 'axf_order'


class orderAndGood(models.Model):
    o_Number = models.ForeignKey(OrderList)
    o_goods = models.ForeignKey(Axf_goods)
    o_count = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_orderAndGoods'
