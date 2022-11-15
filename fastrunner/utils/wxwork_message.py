import time
import json
import base64
import hashlib
import requests

URL = "https://api.hiflow.tencent.com/engine/webhook/31/1592124760872931330"  # Webhook地址


def post(url, data=None):
    """发送POST请求"""
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    r = json.loads(r.text)
    return r


def text(content, mentioned_list=[], mentioned_mobile_list=[]):
    """文本类型

    :param content: 文本内容
    :param mentioned_list: userid列表，@某人，@all为提醒所有人
    :param mentioned_mobile_list: 手机号列表，@某人，@all为提醒所有人
    """
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list,
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }
    return post(URL, data)


def markdown(markdown):
    """Markdown类型

    :param markdown: Markdown内容。支持标题、加粗、链接、行内代码、引用、字体颜色
    """
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown
        }
    }
    return post(URL, data)


def image(file):
    """图片类型

    :param file: 图片路径
    """
    with open(file, "rb") as f:
        _base64 = f.read()
        md5 = hashlib.md5(_base64).hexdigest()
        _base64 = base64.b64encode(_base64).decode("utf-8")
    data = {
        "msgtype": "image",
        "image": {
            "base64": _base64,
            "md5": md5
        }
    }
    return post(URL, data)


def news(title, url, description=None, picurl=None):
    """图文类型

    :param title: 标题
    :param url: 点击后跳转的链接
    :param description: 描述
    :param picurl: 图片链接
    """
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": description,
                    "url": url,
                    "picurl": picurl
                }
            ]
        }
    }
    return post(URL, data)


def sleep(second=60, minute=0, hour=0, day=0):
    """定时任务"""
    secs = second + minute * 60 + hour * 3600 + day * 86400
    time.sleep(secs)


if __name__ == "__main__":
    """文本类型"""
    print(text("Hello World!"))
    print(text("Hello World!", mentioned_list=["wangqing"]))
    print(text("Hello World!", mentioned_mobile_list=["13000000000"]))

    """Markdown类型"""
    print(markdown("# 一级标题\n ## 二级标题"))
    print(markdown("**Hello World!**"))
    print(markdown("[百度一下，你就知道](http://www.baidu.com/)"))
    print(markdown("`code`"))
    print(markdown("> 引用文字"))
    print(markdown('<font color="info">绿色</font>\n <font color="comment">灰色</font>\n <font color="warning">橙红色</font>'))

    """图片类型"""
    print(image("1.jpg"))

    """图文类型"""
    print(news("百度一下，你就知道", "http://www.baidu.com/",
               description="百度搜索是全球最大的中文搜索引擎，2000年1月由李彦宏、徐勇两人创立于北京中关村",
               picurl="https://s1.ax1x.com/2020/07/08/UEL956.jpg"))

    """定时任务"""
    from datetime import datetime

    while True:
        print(text(str(datetime.now())))
        sleep(10)
