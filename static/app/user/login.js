function fromsubmit() {
    $pass = $('#password')
    passwd = $pass.val();
//    将密码进行MD5处理
    md5passwd = md5(passwd)

    $pass.val(md5passwd)

    return true
}