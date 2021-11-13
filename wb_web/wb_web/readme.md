## 后端接口

```
POST：
    /picture_get_data：获取图片设置数据
        上报数据：json串 {"data": data}
            data：1、柔和 2、标准 3、艳丽
        回应：json串 {"eCscMatrix": 3, "Luma": 40, "Contrast": 30, "Hue": 50, "Saturation": 50, "Sharpness": 30}
            eCscMatrix：忽略
            Luma：亮度
            Contrast：对比度
            Hue：色相
            Saturation：饱和度
            Sharpness：锐度

    /LumaCurveSet_get_data：获取亮度曲线数据
        上报数据：无
        回应：json串 {"Node1": 10, "Node2": 30, "Node3": 50, "Node4": 75, "Node5": 90}
            Noden：对应点的值

    /wb_get_data：获取白平衡数据
        上报数据：json串 {"data": data}
            data：1、冷色 2、标准 3、暖色
        回应：json串 {"RedOffset": 0, "GreenOffset": 0, "BlueOffset": 0, "RedColor": 200, "GreenColor": 128, "BlueColor": 128}

    /LumaCurveSet：提交亮度曲线设置值
        上报数据：表单 "Node1=10&Node2=30&Node3=50&Node4=75&Node5=90" 

    /test_picture_set：设置显示那张测试图片
        上报数据：json串 {"data": data}
            data：1、测试图片一 2、测试图片二 3、测试图片三
        回应数据：无

    /picture_choose_3
    /picture_choose_2
    /picture_choose_1：提交图像设置参数，后缀数字代表上面的1、柔和 2、标准 3、艳丽
        上报数据：表单"Luma=40&Contrast=30&Hue=50&Saturation=50&Sharpness=30" 
        回应数据：无

    /wb_choose_3
    /wb_choose_2
    /wb_choose_1：提交白平衡设置参数，后缀数字代表上面的1、冷色 2、标准 3、暖色
        上报数据：表单"RedOffset=0&GreenOffset=0&BlueOffset=0&RedColor=200&GreenColor=128&BlueColor=128" 
        回应数据：无
```
## 参考资料
1、ini解析库configparser相关资料
https://www.jianshu.com/p/417738fc9960
https://www.jianshu.com/p/3e4f10bfac8d
2、BaseHTTPRequestHandler相关资料
[init](http://donghao.org/2015/06/18/override-the-__init__-of-basehttprequesthandler-in-python/)
https://www.jianshu.com/p/4c9ee53dc1cd
3、修饰器
https://blog.csdn.net/qq_42698087/article/details/95929632