$(function () {
    $("#type_container").hide();
     $("#allsortrule").hide();

//  给 全部类型 设置点击事件 控制隐藏
    $("#allType").click(function () {
        $("#type_container").show();
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-chevron-up")
        $("#allsortrule").hide();
        $("#sortrule_g").removeClass().addClass("glyphicon glyphicon-chevron-down")


    });

    $("#type_container").click(function () {
        $(this).hide();
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-chevron-down")

    });


    $("#allsort").click(function () {
        $("#allsortrule").show();
        $("#sortrule_g").removeClass().addClass("glyphicon glyphicon-chevron-up")
        $("#type_container").hide();
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-chevron-down")

    });

    $("#allsortrule").click(function () {
        $("#allsortrule").hide();
        $("#sortrule_g").removeClass().addClass("glyphicon glyphicon-chevron-down")

    });


    // +  按钮(添加到购物车)
    $('.addcart').click(function () {
        //获取商品id
        goodsid = $(this).attr('goodsid');

        $this = $(this);
        urlpath = '/axf/addcart';

        //ajax 请求
        $.getJSON(urlpath,{'goodsid':goodsid},function (data) {
                if (data['code'] == 302){
                    window.open('/axf/login',target='_self')
                }else if(data['code'] == 201){
                    $this.prev('span').html(data['num'])
                }
        })
    })

      //将购物车中的该商品减少一个

    $('.subcart').click(function () {
    //    获取商品ID
        goodsid = $(this).attr('goodsid');

        $this = $(this);
        urlpath = '/axf/subcart';
    //    AJAX请求
        $.getJSON(urlpath,{'goodsid':goodsid},function (data) {
                if (data['code'] == 302){
                    window.open('/axf/login',target='_self')
                }else if(data['code'] == 200){
                    $this.next('span').html(data['num'])
                }
        })
    })
});






