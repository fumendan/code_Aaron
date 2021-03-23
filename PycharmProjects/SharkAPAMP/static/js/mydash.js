$(function () {
    Init();
    function Init () {
        $("#a_auto_click").click();
    auto_active();
    //AssetView3d()
    GetAssetInfo();
    }


    function GetAssetInfo() {
        alert('----ok');

        $.getJSON("/cmdb/dash_board.html/", function (callback) {

            PieView(callback);
        });
    };


    function auto_active() {
        var c_active = $(".my-menu a[href='{{ request.path }}']");
        c_active.parent().addClass('active');
        c_active.parent().parent().parent().addClass('active');
        highchart()
    };

    function PieView(charts_data) {
            $('#pie_container').highcharts({
                chart: {
                    type: 'pie',
                    options3d: {
                        enabled: true,
                        alpha: 45,
                        beta: 0
                    }
                },
                title: {
                    text: '2014年某网站不同浏览器访问量占比'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        depth: 35,
                        dataLabels: {
                            enabled: true,
                            format: '{point.name}'
                        }
                    }
                },
                series: [{
                    type: 'pie',
                    name: '3D饼图',
                    data: charts_data
                }]
            });
        };

    function highchart() {
        var options = {
            chart: {
                type: 'column',
                options3d: {
                    enabled: true,
                    alpha: 15,
                    beta: 15,
                    viewDistance: 25,
                    depth: 40
                },
                marginTop: 80,
                marginRight: 40
            },
            title: {
                text: '以性别划分的水果消费总量'
            },
            xAxis: {
                categories: ['苹果', '橘子', '梨', '葡萄', '香蕉']
            },
            yAxis: {
                allowDecimals: false,
                min: 0,
                title: {
                    text: '水果数量'
                }
            },
            tooltip: {
                headerFormat: '<b>{point.key}</b><br>',
                pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: {point.y} / {point.stackTotal}'
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    depth: 40
                }
            },
            series: [{
                name: '小张',
                data: [5, 3, 4, 7, 2],
                stack: 'male'
            }, {
                name: '小王',
                data: [3, 4, 4, 2, 5],
                stack: 'male'
            }, {
                name: '小彭',
                data: [2, 5, 6, 2, 1],
                stack: 'female'
            }, {
                name: '小潘',
                data: [3, 0, 4, 4, 3],
                stack: 'female'
            }]
        };
        var chart = Highcharts.chart('container', options);
    };


    function AssetView(chart_data) {


        //  注意下面的关键字，若是关键字写错了，是不会有报错提示的，只会不生效
        //绘制柱状图
        // 基于准备好的 dom， 初始化 echarts 实例
        var myChart = echarts.init(document.getElementById('dashboard-yange-1'));
        // 指定图表的配置项和数据
        var option = {
            tooltip: {}, // 提示信息，当鼠标放在每个柱子上，会提示出当前项的数值
            legend: {     // 说明信息，图例的意思，表示此张图表代表的项目本意；如销量，占比，排名等
                data: ['资产类型']   //
            },
            xAxis: {
                data: chart_data.names
            }, // X 轴
            yAxis: {},      // Y 轴
            series: [{     // 系列
                name: '数量', // 和上面的 legend 同名会展示在 提示信息中
                type: 'bar',
                data: chart_data.data
            }]
        };
        // 使用刚指定的配置项和数据绑定到实例化的图表上
        myChart.setOption(option);
        // 函数体结束
    }

    // 函数结束

    function AssetView3d() {
        var my3dchart = echarts.init(document.getElementById('container2'));
        var hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
            '7a', '8a', '9a', '10a', '11a',
            '12p', '1p', '2p', '3p', '4p', '5p',
            '6p', '7p', '8p', '9p', '10p', '11p'];
        var days = ['Saturday', 'Friday', 'Thursday',
            'Wednesday', 'Tuesday', 'Monday', 'Sunday'];

        var data = [[0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0], [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3], [0, 16, 4], [0, 17, 6], [0, 18, 4], [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5], [1, 0, 7], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0], [1, 6, 0], [1, 7, 0], [1, 8, 0], [1, 9, 0], [1, 10, 5], [1, 11, 2], [1, 12, 2], [1, 13, 6], [1, 14, 9], [1, 15, 11], [1, 16, 6], [1, 17, 7], [1, 18, 8], [1, 19, 12], [1, 20, 5], [1, 21, 5], [1, 22, 7], [1, 23, 2], [2, 0, 1], [2, 1, 1], [2, 2, 0], [2, 3, 0], [2, 4, 0], [2, 5, 0], [2, 6, 0], [2, 7, 0], [2, 8, 0], [2, 9, 0], [2, 10, 3], [2, 11, 2], [2, 12, 1], [2, 13, 9], [2, 14, 8], [2, 15, 10], [2, 16, 6], [2, 17, 5], [2, 18, 5], [2, 19, 5], [2, 20, 7], [2, 21, 4], [2, 22, 2], [2, 23, 4], [3, 0, 7], [3, 1, 3], [3, 2, 0], [3, 3, 0], [3, 4, 0], [3, 5, 0], [3, 6, 0], [3, 7, 0], [3, 8, 1], [3, 9, 0], [3, 10, 5], [3, 11, 4], [3, 12, 7], [3, 13, 14], [3, 14, 13], [3, 15, 12], [3, 16, 9], [3, 17, 5], [3, 18, 5], [3, 19, 10], [3, 20, 6], [3, 21, 4], [3, 22, 4], [3, 23, 1], [4, 0, 1], [4, 1, 3], [4, 2, 0], [4, 3, 0], [4, 4, 0], [4, 5, 1], [4, 6, 0], [4, 7, 0], [4, 8, 0], [4, 9, 2], [4, 10, 4], [4, 11, 4], [4, 12, 2], [4, 13, 4], [4, 14, 4], [4, 15, 14], [4, 16, 12], [4, 17, 1], [4, 18, 8], [4, 19, 5], [4, 20, 3], [4, 21, 7], [4, 22, 3], [4, 23, 0], [5, 0, 2], [5, 1, 1], [5, 2, 0], [5, 3, 3], [5, 4, 0], [5, 5, 0], [5, 6, 0], [5, 7, 0], [5, 8, 2], [5, 9, 0], [5, 10, 4], [5, 11, 1], [5, 12, 5], [5, 13, 10], [5, 14, 5], [5, 15, 7], [5, 16, 11], [5, 17, 6], [5, 18, 0], [5, 19, 5], [5, 20, 3], [5, 21, 4], [5, 22, 2], [5, 23, 0], [6, 0, 1], [6, 1, 0], [6, 2, 0], [6, 3, 0], [6, 4, 0], [6, 5, 0], [6, 6, 0], [6, 7, 0], [6, 8, 0], [6, 9, 0], [6, 10, 1], [6, 11, 0], [6, 12, 2], [6, 13, 1], [6, 14, 3], [6, 15, 4], [6, 16, 0], [6, 17, 0], [6, 18, 0], [6, 19, 0], [6, 20, 1], [6, 21, 2], [6, 22, 2], [6, 23, 6]];
        option = {
            tooltip: {},
            visualMap: {
                max: 20,
                inRange: {
                    color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                }
            },
            xAxis3D: {
                type: 'category',
                data: hours
            },
            yAxis3D: {
                type: 'category',
                data: days
            },
            zAxis3D: {
                type: 'value'
            },
            grid3D: {
                boxWidth: 200,
                boxDepth: 80,
                viewControl: {
                    projection: 'orthographic'
                },
                light: {
                    main: {
                        intensity: 1.2,
                        shadow: true
                    },
                    ambient: {
                        intensity: 0.3
                    }
                }
            },
            series: [{
                type: 'bar3D',
                data: data.map(function (item) {
                    return {
                        value: [item[1], item[0], item[2]],
                    }
                }),
                shading: 'lambert',

                label: {
                    textStyle: {
                        fontSize: 16,
                        borderWidth: 1
                    }
                },

                emphasis: {
                    label: {
                        textStyle: {
                            fontSize: 20,
                            color: '#900'
                        }
                    },
                    itemStyle: {
                        color: '#900'
                    }
                }
            }]
        };

        my3dchart.setOption(option);


    };


    function MyPie() {
        /********************************************/
        //绘制南丁格尔图
        var myPieChart = echarts.init(document.getElementById('pie'));

        myPieChart.setOption({

            tooltip: {
                formatter: "{a}<br/>{b}:{c} ({d}%)"
            },
            series: [
                {
                    name: '应用占用办百分比展示',
                    type: 'pie',
                    radius: ['90%', '50%'], // 外圆占比，内圆空白占比
                    data: [
                        {value: 305, name: '视频'},
                        {value: 265, name: '游戏'},
                        {value: 350, name: '工单管理'},
                        {value: 335, name: '国际支付'},
                        {value: 400, name: '搜索'}
                    ],
                    /*
                    * 这里data属性值不像入门教程里那样每一项都是单个数值，
                    * 而是一个包含 name 和 value 属性的对象，
                    * ECharts 中的数据项都是既可以只设成数值，
                    * 也可以设成一个包含有名称、该数据图形的样式配置、标签配置的对象
                    * */
                    roseType: 'angle',  // ECharts 中的饼图也支持通过设置 roseType 显示成南丁格尔图；
                    // 南丁格尔图会通过半径的长度表示数据的大小。。
                    // angle 翻译为： 角度

                    /*
                    * ECharts 中有一些通用的样式，诸如阴影、透明度、颜色、边框颜色、边框宽度等，
                    * 这些样式一般都会在系列的 itemStyle 里设置.
                    * itemStyle都会有normal和emphasis两个选项，normal选项是正常展示下的样式，
                    * emphasis是鼠标 hover 时候的高亮样式。
                    * 可能更多的时候是 hover 的时候通过阴影突出。
                     */
                    /*itemStyle:{
                        normal: {
                            // 设置扇形颜色
                            color: '#c23531',
                            shadowBlur: '200',
                            shadowColor: 'rgba(0,0,0,0.5)',
                        },*/
                    /*
                    emphasis: {
                        shadowBlur: 200,  // 阴影大小
                        shadowOffsetX: 0, //  阴影水平方向的偏移
                        shardowOffsetY: 0, // 阴影垂直方向的偏移
                        shadowColor: 'rgba(0,0,0,0.5)',  // 阴影颜色
                        textStyle: {       // 文本颜色局部设置
                             color: 'rgba(255, 255, 255, 0.3)',
                        },
                    },
                {,*/
                    labelLine: {
                        normal: {
                            lineStyle: {  // 饼图的话还要将标签的视觉引导线的颜色设为浅色
                                color: 'rgba(255,25,255,0.3)',
                            },
                        },
                    },

                },
            ],
            //backgroundColor: '#2c343c', //背景色是全局的，所以直接在 option 下设置 backgroundColor
            textStyle: {                  // 文本颜色全局设置
                color: 'rgba(255, 255, 255, 2)'
            },

            /*
            * ECharts 中每个扇形颜色的可以通过分别设置 data 下的数据项实现。
            * data: [{
            value:400,
            name:'搜索引擎',
            itemStyle: {
                normal: {
                    color: '#c23531'
                }
            }
            } , ...]
            *但是这次因为只有明暗度的变化，所以有一种更快捷的方式是通过 visualMap 组件将数值的大小映射到明暗度
            * */

            visualMap: {
                // 不显示 visualMap 组件，只用于明暗度的映射
                show: false,
                // 映射的最小值为 80
                min: 80,
                // 映射的最大值为 600
                max: 600,
                inRange: {
                    // 明暗度的范围是 0 到 1
                    colorLightness: [0, 1],
                },
            },
        })
    }


}());