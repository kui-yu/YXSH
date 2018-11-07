$(function () {

      // 将购物车列表商品数量加一
      $('.addcartGoodsnum').click(function () {
        //获取商品id
        cartid = $(this).attr('cartid');
        $this = $(this);
        urlpath = '/axf/addcartGoodsnum';

        //ajax 请求
        $.getJSON(urlpath,{'cartid':cartid},function (data) {
                if(data['code'] == 200){
                    $this.prev('span').html(data['num'])
                }
        })
      });


    // 将购物车列表商品数量减一
     $('.subcartGoodsnum').click(function () {
        //获取商品id
        cartid = $(this).attr('cartid');
        $this = $(this);
        urlpath = '/axf/subcartGoodsnum';

        //ajax 请求
        $.getJSON(urlpath,{'cartid':cartid},function (data) {
                if(data['code'] == 200){
                    $this.next('span').html(data['num'])
                }else if(data['code'] == 300){
                    $this.parents('li').remove()
                }
        })
      });


     // 勾选按钮的点击事件
     $('.selectButton').click(function () {
         $this = $(this);
         cartid = $this.parents('li').attr('cartid');
         urlpath ='/axf/changeSelect';
         $.getJSON(urlpath,{'cartid':cartid},function (data) {
             if (data['code']==200){
                 // alert(data['isselect']);
                 if (data['isselect']){
                     $this.html('<span>√</span>')
                     $this.attr('isselect','True')
                 }else{
                     $this.html('<span></span>')
                     $this.attr('isselect','False')
                 }
             //    是否全选
                 if(data['isAllSelect']){
                     $('#allSelectButton').html('<span>√</span>')
                 }else{
                     $('#allSelectButton').html('<span></span>')
                 }

             }
         })

     });

     //全选按钮的点击事件
     $('#allSelectButton').click(function () {
     /*
  全选按钮的点击情况：1.只要有一个商品没有选中,点击全选按钮,所有的商品变为选中状态
                   2.当所有商品处于选中状态时,点击全选按钮, 所有的商品处于未被选中状态
     */

     //第一步操作 获取所有的商品的选择状态
     //    选中的
        var isselectlist = [];
        //选中的
        var noselectlist =[];
         $('.selectButton').each(function () {
             //获得商品id
             cartid = $(this).parents('li').attr('cartid');
             //获得选中状态
             isselect = $(this).attr('isselect');
             if (isselect == 'True'){
                 isselectlist.push(cartid)
             }else{
                 noselectlist.push(cartid)
             }
         });
         // console.log(isselectlist);
         // console.log(noselectlist);
         if(noselectlist.length==0 && isselectlist.length >=1 ){
         //    全部选中
              urlpath = '/axf/changaManyButton';
              $.getJSON(urlpath,{'cartidlist':isselectlist.join('#'),'flag':2},function (data) {
                  if (data['code']==200){
                      $('.selectButton').each(function () {
                          $(this).html('<span></span>');
                          $(this).attr('isselect','False')
                      });
                      $('#allSelectButton').html('<span></span>')
                  }
              })
         }else{
         //    只要有一个不选中
             urlpath = '/axf/changaManyButton';
             //将未选中的变为选中的
             $.getJSON(urlpath,{'cartidlist':noselectlist.join('#'),'flag':1},function (data) {
                    if (data['code']==200){
                        $('.selectButton').each(function () {
                            $(this).html('<span>√</span>');
                            $(this).attr('isselect','True')
                        });
                        $('#allSelectButton').html('<span>√</span>')
                    }
             })
         }
     })



//    生成订单点击事件
    $('#createOrder').click(function () {
        var selectList=[];
        $('.selectButton').each(function () {
            isselect = $(this).attr('isselect');
            cartid = $(this).parents('li').attr('cartid');
            if(isselect == 'True'){
                selectList.push(cartid)
            }
        });
        // console.log(selectList)
        if(selectList.length == 0){
            alert('没选中任何商品')
        }else{
                urlpath = '/axf/createOrder';
            $.getJSON(urlpath,{'selectList':selectList.join('#')},function (data) {
                    if(data['code']==200){
                    //    订单创建成功
                        window.open('/axf/showOrder',target='_self')
                    }
            })
        }

    })

});