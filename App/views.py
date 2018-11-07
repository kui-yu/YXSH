import uuid

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from App.models import Axf_wheel, Axf_nav, Axf_mustBuy, Axf_shop, Axf_mainshow, Axf_foodtypes, Axf_goods, UserModel, \
    GoodsCart, OrderList, orderAndGood


def home(request):
    wheels = Axf_wheel.objects.all()
    navs = Axf_nav.objects.all()
    mustBuys = Axf_mustBuy.objects.all()
    shop = Axf_shop.objects.all()
    shop0 = shop[0]
    shop1_2 =shop[1:3]
    shop3_6 = shop[3:7]
    shop7_10 = shop[7:11]


    mainshows = Axf_mainshow.objects.all()

    data = {
        'wheels':wheels,
        'navs':navs,
        'mustBuys':mustBuys,
        'shop0':shop0,
        'shop1_2':shop1_2,
        'shop3_6':shop3_6,
        'shop7_10':shop7_10,
        'mainshows':mainshows,
    }
    return render(request, 'home/home.html',context=data)


def market_by_typeid(request,typeid,childtypeid,sortType):
    foodtypes = Axf_foodtypes.objects.all()


    if childtypeid == "0":
        goods = Axf_goods.objects.filter(categoryid=typeid)
    else:
        goods = Axf_goods.objects.filter(categoryid=typeid).filter(childcid=childtypeid)

    sortType = str(sortType)
    if sortType == "0":  # 综合排序
        pass
    elif sortType == "1":  # 销量排序
        goods = goods.order_by("productnum")
    elif sortType == "2":  # 价格降序
        goods = goods.order_by("-price")
    elif sortType == "3":  # 价格升序
        goods = goods.order_by("price")



    # 获取typeid的所有子分类的信息
    food_type = Axf_foodtypes.objects.filter(typeid=typeid).first()

    childtypenames = food_type.childtypenames.split('#')

    childNameAndIds = []
    for childtype in childtypenames:
        childNameAndId = childtype.split(':')
        childNameAndIds.append(childNameAndId)


    data = {
        'foodtypes': foodtypes,
        'goods': goods,
        'currentType':typeid,
        'childNameAndIds':childNameAndIds,
        "currentChildid": childtypeid,
    }
    return render(request, 'market/market.html', context=data)


def market(request):
    return HttpResponseRedirect(reverse('axf:market_by_typeid',args=(104749,0,0)))

# 购物车
def cart(request):
    userid = request.session.get('user_id')
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
        carts = GoodsCart.objects.filter(c_user=user)
        totalNumberPrice = totalAndPrice(user)
        # 订单是否全部选中
        isAllSelect = True

        for cart in carts:
            if not cart.c_isselect:  #没有选中
                isAllSelect = False


        data = {
            'carts':carts,
            'is_allselect':isAllSelect,
            'selectCount':totalNumberPrice.get('selectCount'),
            'totalPrice':totalNumberPrice.get('totalPrice'),
        }

        return render(request, 'cart/cart.html',context=data)
    else:
        return HttpResponseRedirect(reverse('axf:login'))

# 添加商品到购物车
def addcart(request):
    # 获取商品的id  商品数量  选中状态  用户id
    # 获得用户信息
    data={}
    user_id = request.session.get('user_id')
    if user_id:
        user = UserModel.objects.filter(pk=user_id).first()
    else:
        data['code']=302
        data['msg'] = '登录成功'
        return  JsonResponse(data)

    goodsid = request.GET.get('goodsid')
    goods = Axf_goods.objects.filter(pk=goodsid).first()
    # 获取当前用户的购物车数据
    cartRes = GoodsCart.objects.filter(c_user=user).filter(c_goods=goods)
    if cartRes:
        cart = cartRes.first()
        cart.c_num +=1
        data['code'] = 201
        data['msg'] = '加入购物车成功'
        data['num'] = cart.c_num
        cart.save()
    else:
        cart = GoodsCart()
        cart.c_user = user
        cart.c_goods = goods
        cart.c_num = 1
        cart.c_isselect = True
        cart.save()
        data['code'] = 201
        data['msg'] = '加入购物车成功'
        data['num'] = 1
    return JsonResponse(data)


# 从购物车移除商品
def subcart(request):
    # 判断是否登录
    data = {}
    user_id = request.session.get('user_id')
    if user_id:
        user = UserModel.objects.filter(pk=user_id).first()
    else:
        data['code'] = 302
        data['msg'] = '登录成功'
        return JsonResponse(data)
    goodsid = request.GET.get('goodsid')
    goods = Axf_goods.objects.filter(pk = goodsid).first()
    # 获得当前用户下的购物车数据
    cartRes = GoodsCart.objects.filter(c_user=user).filter(c_goods=goods)
    if cartRes:
        cart = cartRes.first()
        # cart  = GoodsCart()
        if cart.c_num ==1:
            cart.delete()
            data['code'] =200
            data['msg'] = '操作成功'
            data['num'] = 0
        else:
            cart.c_num -=1
            cart.save()
            data['code'] = 200
            data['msg'] = '操作成功'
            data['num'] = cart.c_num
    else:#不存在
        data['code'] = 200
        data['msg'] = '操作成功'
        data['num'] = 0
    return JsonResponse(data)


# 将购物车里面的商品数量加一
def addcartGoodsnum(request):
    # 获得cardid就行
    data={}
    cartid  = request.GET.get('cartid')
    cart = GoodsCart.objects.filter(pk=cartid).first()
    cart.c_num +=1
    cart.save()
    data['code'] = 200
    data['msg'] = '购物车商品数量增加成功'
    data['num'] = cart.c_num
    return JsonResponse(data)

# 将购物车里面的商品数量减一
def subcartGoodsnum(request):
    data = {}
    cartid = request.GET.get('cartid')
    cart = GoodsCart.objects.filter(pk=cartid).first()
    # cart = GoodsCart()
    if cart.c_num == 1:
       cart.delete()
       data['code'] = 300
       data['msg'] = '购物车商品数量减少成功'
       data['num'] = 0
    elif cart.c_num >1:
        cart.c_num -=1
        cart.save()
        data['code'] = 200
        data['msg'] = '购物车商品数量减少成功'
        data['num'] = cart.c_num

    return JsonResponse(data)


# 改变购物车选中状态
def changeSelect(request):
    cartid = request.GET.get('cartid')
    cart = GoodsCart.objects.filter(pk=cartid).first()
    cart.c_isselect = not cart.c_isselect
    # print(cart.c_isselect)
    cart.save()
    # 是否全选
    userid = request.session.get('user_id')
    user = UserModel.objects.filter(pk=userid)
    # 获得该用户所有的购物车数据
    carts = GoodsCart.objects.filter(c_user=user)
    isAllSelect = True
    for cart1 in carts:
        if not cart1.c_isselect:
            isAllSelect = False

    data={
        'code':200,
        'msg':'修改状态成功',
        'isselect':cart.c_isselect,
        'isAllSelect':isAllSelect
    }
    return JsonResponse(data)

# 改变多条商品的选中状态
def changaManyButton(request):
    cartidlist = request.GET.get('cartidlist').split('#')
    flag = request.GET.get('flag')
    data = {}
    for cartid in cartidlist:
        cart = GoodsCart.objects.filter(pk=cartid).first()
        if flag == '1':
            cart.c_isselect = True
            data['msg'] = '全部变为选中'
        elif flag =='2':
            cart.c_isselect = False
            data['msg'] = '全部变为未选中'
        cart.save()

    data['code']=200

    return JsonResponse(data)





# 我的
def mine(request):
    # 判断是否登录
    userid = request.session.get('user_id')
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
        imgpath = '/static/upload/'+user.u_img.url
        data = {
            'user':user,
            'imgpath':imgpath,
        }
        return render(request,'mine/mine.html',context=data)
    else:
        return render(request, 'mine/mine.html',context={'user':None})




# 注册
def register(request):
    method = request.method
    if method =='GET':
        return render(request, 'user/register.html')
    elif method == 'POST':
        uername = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        imgFile = request.FILES.get('imgFile')
        user = UserModel()
        user.u_name = uername
        user.u_password = password
        user.u_email = email
        user.u_img = imgFile
        user.save()
        return HttpResponseRedirect(reverse('axf:login'))

# 检测用户名是否存在
def checkUser(request):
    username = request.GET.get('username')
    userquery = UserModel.objects.filter(u_name=username)
    data = {}
    if userquery.exists():
        data['code'] = 200
        data['msg'] = '该用户名已经存在'

    else:
        data['code'] = 300
        data['msg'] = '该用户名不存在'
    return JsonResponse(data)

# 登录
def login(request):
    method = request.method
    if method == 'GET':
        return render(request,'user/user_login.html')
    elif method == 'POST':
        uername = request.POST.get('username')
        password = request.POST.get('password')
        user = UserModel.objects.filter(u_name=uername).first()
        if user:
            if user.u_password==password:
                request.session['user_id'] = user.id

                return HttpResponseRedirect(reverse('axf:mine'))

        else:
            return render(request, 'user/user_login.html')


# 退出帐号
def outlogin(request):
    # 清楚帐号信息
    request.session.flush()
    return  HttpResponseRedirect(reverse('axf:login'))

# 计算选中的数量和总价
def totalAndPrice(user):
#     计算选中数量
    cartsSelect = GoodsCart.objects.filter(c_user=user).filter(c_isselect=True)
    # 计算选中数量的总价
    totalPrice = 0
    selectCount = 0
    for cart in cartsSelect:
        goods = cart.c_goods
        totalPrice += goods.price * cart.c_num
        selectCount +=cart.c_num
    return {'selectCount':selectCount,'totalPrice':totalPrice}


#
def createOrder(request):

    user_id = request.session.get('user_id')
    user = UserModel.objects.filter(pk = user_id).first()
    #创建订单表
    order = OrderList()
    order.o_Number = str(uuid.uuid4())
    order.o_user = user    #绑定用户
    order.o_status = 1    #未付款状态
    order.save()

    # 创建订单用户关系表
    # 获得购物车中选中的商品
    cartids = request.GET.get('selectList').split('#')
    for cartid in cartids:
        cart = GoodsCart.objects.filter(pk=cartid).first()
        # cart = GoodsCart()
        OrderAndGood = orderAndGood()
        OrderAndGood.o_Number =  order   #绑定订单号
        OrderAndGood.o_goods = cart.c_goods     #绑定商品
        OrderAndGood.o_count = cart.c_num    #绑定商品数量
        OrderAndGood.save()
        cart.delete()

        data = {
            'code':200,
            'msg':'订单创建完成',
        }
    return JsonResponse(data)


def showOrder(request):
    return render(request, 'mine/showOrder.html')