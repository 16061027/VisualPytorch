function getQueryObject(url) {
    url = url == null ? window.location.href : url;
    var search = url.substring(url.lastIndexOf("?") + 1);
    var obj = {};
    //一个经典漂亮的正则表达式
    var reg = /([^?&=]+)=([^?&=]*)/g;
    search.replace(reg, function (rs, $1, $2) {
        var name = decodeURIComponent($1);
        var val = decodeURIComponent($2);
        val = String(val);
        obj[name] = val;
        return rs;
    });
    return obj;
}

function login() {

    var username = $("#username_log").val();
    var password = $("#pwd_log").val();

    var data = {
        "username": username,
        "password": password
    };

    $.ajax({
        type: 'POST',
        url: 'api/user/login/',
        async:false,//note：这里ajax必须为同步请求，两个ajax必须先拿token,再拿用户信息
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function (data_return) {
                var token = data_return["token"];
                window.sessionStorage.setItem('token', token)
        },
        error: function (data_return) {
            alert("账号密码错误，请重新登录");
            console.log(data_return["responseText"])
        }
    });
    $.ajax({
        type: 'GET',
        async:false,
        url: 'api/user/info/',
        beforeSend: function (XMLHttpRequest) {
            var token = window.sessionStorage.getItem('token');
            if (token != null) {
                XMLHttpRequest.setRequestHeader("Authorization", "JWT " + token)
            }
        },
        success: function (data_return) {
            window.sessionStorage.setItem('userinfo', JSON.stringify(data_return));
             window.location.href = "canvas.html"
        }
    });
}


function register() {
    //todo:加正则判断
    var username = $("#username_reg").val();
    var password = $("#pwd_reg").val();
    if ($('#pwd_confirm_reg').val() != password) {
        alert("两次输入密码不一致");
        return;
    }
    var email = $("#email_reg").val();

    var data = {
        "username": username,
        "email": email,
        "password": password
    };

    $.ajax({
        type: 'POST',
        url: 'api/user/register/',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function (data_return) {
                var token = data_return["token"];
                window.sessionStorage.setItem('token', token);
                window.sessionStorage.setItem('userinfo', JSON.stringify(data_return));
                window.location.href = "canvas.html"
        },
        error: function (data_return) {
            alert("用户名或邮箱已被注册")
            console.log(data_return["responseText"])
        }
    })

}

function logout() {
    window.sessionStorage.removeItem('token');
    window.sessionStorage.removeItem('userinfo');
    $("#user_nav").hide();
    $("#login_nav").show();
    alert("用户已登出")

}