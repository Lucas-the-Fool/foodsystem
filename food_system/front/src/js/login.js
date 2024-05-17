var LoginHandler = function () {
};

LoginHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on("click", function (event) {
        event.preventDefault();
        var username = $("#username").val();
        var password = $("#password").val();
        var user_type = $("#select-user-type").val();
        $.ajax({
            url: "/login/",
            type: 'POST',
            data: {
                username,
                password,
                user_type
            },
            success: function (result) {
                if (result['code'] == 200) {
                    alert('Login success');
                    window.location = "/"
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

LoginHandler.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var handler = new LoginHandler();
    handler.run();
});