from django.conf.urls import url, include
from django.contrib import admin

from App import views

urlpatterns = [
    url(r'^home/',views.home,name='home'),
    url(r'^market/',views.market,name='market'),
    url(r'^market_by_typeid/(\d+)/(\d+)/(\d+)',views.market_by_typeid,name='market_by_typeid'),
    # 将商品添加到购物车
    url(r'^addcart/',views.addcart,name='addcart'),
    url(r'^subcart/',views.subcart,name='subcart'),
    # 购物车---添加--移除
    url(r'^cart/',views.cart,name='cart'),
    # 将购物车里面的商品数量加一
    url(r'^addcartGoodsnum/', views.addcartGoodsnum, name='addcartGoodsnum'),
    url(r'^subcartGoodsnum/', views.subcartGoodsnum, name='subcartGoodsnum'),
    url(r'^changeSelect/', views.changeSelect, name='changeSelect'),
    url(r'^changaManyButton/', views.changaManyButton, name='changaManyButton'),
    url(r'^createOrder/', views.createOrder, name='createOrder'),
    url(r'^showOrder/', views.showOrder, name='showOrder'),




    # 我的---注册--登录--退出登录
    url(r'^mine/',views.mine,name='mine'),
    url(r'^register/',views.register,name='register'),
    url(r'^checkUser/',views.checkUser),
    url(r'^login/',views.login,name='login'),
    url(r'^outlogin/',views.outlogin,name='outlogin'),




]