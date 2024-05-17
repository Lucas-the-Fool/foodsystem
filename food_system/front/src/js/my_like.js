var MyLike = function () {
};

MyLike.prototype.listenDeleteEvent = function () {
    $(".delete-like-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var like_id = $this.attr('like-id');
        $.ajax({
            url: "/my_like/",
            type: 'POST',
            data: {
                like_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('Cancel successfully');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};


MyLike.prototype.run = function () {
    this.listenDeleteEvent();
};


$(function () {
    var handler = new MyLike();
    handler.run();
});