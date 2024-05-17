var MyInfo = function () {
};

MyInfo.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on("click", function (event) {
        event.preventDefault();
        var username = $("#username").val();
        var password = $("#password").val();
        var phone = $("#phone").val();
        var address = $("#address").val();
        $.ajax({
            url: "/my_info/",
            type: 'POST',
            data: {
                username,
                password,
                phone,
                address
            },
            success: function (result) {
                if (result['code'] == 200) {
                    alert('Successful submission');
                    location.reload();
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

MyInfo.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var handler = new MyInfo();
    handler.run();
});