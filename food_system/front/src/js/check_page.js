var CheckPage = function () {
};

var IMAGE_URL = '';
CheckPage.prototype.listenSubmitEvent = function () {
    var uploadBtn = $('#image-input-tag');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        $.ajax({
            'type': 'POST',
            'url': '/img_upload/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    IMAGE_URL = result['image_url'];
                    var img_tag = $('#image-src-tag');
                    img_tag.attr('src', IMAGE_URL)
                }
            }
        })
    })
};

CheckPage.prototype.ImageCheckEvent = function () {
    var checkBtn = $('#check-btn');
    checkBtn.click(function () {
        var image_url = IMAGE_URL;
        $.ajax({
            'type': 'POST',
            'url': '/food_check/',
            data: {
                image_url
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var pred_name = result['pred_name'];
                    alert('Recognition result：' + pred_name)
                }
            }
        })
    })
};

CheckPage.prototype.run = function () {
    this.listenSubmitEvent();
    this.ImageCheckEvent();
};


$(function () {
    var handler = new CheckPage();
    handler.run();
});