var FoodDetail = function () {
};


FoodDetail.prototype.listenScoreEvent = function () {
    $("#score-btn").on("click", function (event) {
        event.preventDefault();
        var score = $("#input-score").val();
        var $this = $(this);
        var food_id = $this.attr('food-id');

        $.ajax({
            url: "/input_score/",
            type: 'POST',
            data: {
                score,
                food_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('Success Evaluation');
                    location.reload();
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

FoodDetail.prototype.listenAddLike = function () {
    $("#add-like-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var food_id = $this.attr('food-id');

        $.ajax({
            url: "/add_like/",
            type: 'POST',
            data: {
                food_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('Add successfully');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

FoodDetail.prototype.listenAddComment = function () {
    $("#add-comment-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var food_id = $this.attr('food-id');
        var content = $('#comment-textarea').val();
        $.ajax({
            url: "/add_comment/",
            type: 'POST',
            data: {
                food_id,
                content
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('release successfully');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};


FoodDetail.prototype.run = function () {
    this.listenAddLike();
    this.listenAddComment();
    this.listenScoreEvent();
};


$(function () {
    var handler = new FoodDetail();
    handler.run();
});