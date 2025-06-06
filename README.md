# yuanshen_wallpaper_downloader

用python的selenium库获取原神官方发布的壁纸（有下载链接下载下载链接，若没有直接下载

详见[https://www.hoyolab.com/creatorCollection/526679](https://www.hoyolab.com/creatorCollection/526679)

环境：

```
pip install selenium numpy wget
```

先运行find.py,在运行find2download.py

<details>

<summary>过时的简介</summary>

PS:本质上是查询一个页面上所有帖子然后逐个分析，所有只要把链接改成其他壁纸帖子合集就可以下载别的hoyolab图片了

感谢copilot解决疑难杂症，selenium文档好少

截止2025/1/8

![image](https://github.com/user-attachments/assets/c1fa7816-228f-4ab8-ac32-f42231edee12)

</details>

用action定时执行任务，获取壁纸并生成展示网页和随机壁纸
感谢万能的copilot！