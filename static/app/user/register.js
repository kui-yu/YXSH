//校验用户名是否存在
//当用户名失去焦点时 且输入框内容发生改变时
 var flag1 = false;
 var flag2 = false;
$(function () {

   $("#username").change(function () {
    //  请求服务器校验...
        username = $(this).val();
        // 参数1: url地址
        // 参数2: data 请求参数  key-value
        // 参数3: callback回调函数, 当请求成功之后调用,data是服务器返回的数据
        // */
        $.getJSON("/axf/checkUser",{"username":username},function (data) {

            $name =  $("#nameError");
            if(data["code"] == 300){
                $name.html('用户名可用').css('color','green')
                flag2 = true
            }else if (data["code"] ==200) {
                $name.html('用户名不可用').css('color','red')
                flag2 = false
            }
        })


    });


//    校验设置的密码两次是否一样
    $('#password2').change(function () {
    //    校验密码的合法性
        passwd1 = $('#password1').val();
        // console.log(passwd1);
        passwd2 = $('#password2').val();
        // console.log(passwd2);
        if(passwd1.length <=6){
            $('#errorMsg').html('密码长度至少为六位').css('color','red');
            flag1 = false;
            return
        }

        if (passwd1 != passwd2){
            $('#errorMsg').html('两次密码输入不一致,请重新设置').css('color','red');
            flag1 = false;
            return
        }

         $('#errorMsg').html('密码合法').css('color','green')
        flag1 = true;
    })

});

//提交之前调用  验证输入的合法性

function fromsubmit() {

    if(!flag1){
        alert('密码不合法,不能提交')
        return false
    }
    if(!flag2){
        alert('用户名不合法,不能提交');
        return false
    }

    password2 = $('#password2').val();
    //将密码进行MD5加密 再加密
    md5res = md5(password2);
    //将密码框中的内容换成
    $('#password2').val(md5res);
    return true
}