$('#login-btn').click(function(){
        let username = $('#username').val();
        let password = $('#password').val();
        let csrf_token = $('#csrf_token').val();
        let username_error = document.getElementById('username-error');
        let password_error = document.getElementById('password-error');
        let login_status = document.getElementById('login-status');

        if(!username || !password){
            if(!username){
                username_error.innerText = "请填写该区域内容";
            } else {
                username_error.innerText = "";
            }

            if(!password){
                password_error.innerText = "请填写该区域内容";
            } else {
                password_error.innerText = "";
            }
            return;
        }

        $.ajax({
            url: "${reverse('dashboard_login')}",
            type: "POST",
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: csrf_token
            },
            success: function(json) {
                let code = json['status']
                if(code<0) {
                    login_status.innerText = "用户不存在，请重试";
                    login_status.setAttribute('class', 'text-danger');
                } else {
                    login_status.innerText = "登录成功，正在跳转";
                    login_status.setAttribute('class', 'text-success');
                    setTimeout(function() {
                        window.location.href = "${to}";
                    }, 2000);
                }
                return ;
            },
            error: function () {
                login_status.innerText = "登录失败，请重试";
                login_status.setAttribute('class', 'text-danger');
                return ;
            }
        });
    });