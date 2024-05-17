var ShowInfo = function () {

    var myChart = echarts.init(document.getElementById('main'));

    $.ajax({
        url: "/view_count/",
        type: 'POST',
        data: {},
        success: function (result) {
            if (result['code'] === 200) {
                option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: result['name_list'],
                            axisTick: {
                                alignWithLabel: true
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
                        }
                    ],
                    series: [
                        {
                            name: 'Number of views',
                            type: 'bar',
                            barWidth: '60%',
                            data: result['count_list']
                        }
                    ]
                };


                myChart.setOption(option);
            } else {
                alert(result['message']);
            }
        }
    });
};


$(function () {
    var handler = new ShowInfo();
});