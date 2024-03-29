from httpx import get as httpx_get
from JianshuResearchTools.user import GetUserName

from register import register_task

"""
监控函数返回值：
- success(bool): 是否成功
- status_code(int): 状态码
- message(str): 说明
"""


@register_task("简书主站监控", "0 1-59 * * * *")  # 每分钟执行一次
def JianshuMainPageMonitor():
    try:
        response = httpx_get("https://www.jianshu.com/")
    except Exception as e:
        success = False
        status_code = -1
        message = str(e)
    else:
        message = ""
        status_code = response.status_code
        if status_code != 200:
            success = False
        else:
            success = True
    return (success, status_code, message)


@register_task("简书 Json API 监控", "0 1-59 * * * *")  # 每分钟执行一次
def JianshuJsonDataAPIMonitor():
    result = GetUserName("https://www.jianshu.com/u/ea36c8d8aa30/")
    if result != "初心不变_叶子":
        success = False
        status_code = -1
        message = "数据不正常"
    else:
        success = True
        status_code = 200
        message = ""
    return (success, status_code, message)


@register_task("贝壳小岛主站监控", "0 0/5 * * * *")  # 每五分钟执行一次
def BeiKeIslandMainPageMonitor():
    try:
        response = httpx_get("http://www.beikeisland.com/index.html")
    except Exception as e:
        success = False
        status_code = -1
        message = str(e)
    else:
        message = ""
        status_code = response.status_code
        if status_code != 200:
            success = False
        else:
            success = True
    return (success, status_code, message)


@register_task("消零派辅助工具监控", "0 0/5 * * * *")  # 每五分钟执行一次
def DisZeroerHelperMainPageMonitor():
    try:
        response = httpx_get("http://120.27.239.120:8601/")
    except Exception as e:
        success = False
        status_code = -1
        message = str(e)
    else:
        message = ""
        status_code = response.status_code
        if status_code != 200:
            success = False
        else:
            success = True
    return (success, status_code, message)


@register_task("简书小工具集监控", "0 0/5 * * * *")  # 每五分钟执行一次
def JianshuMicroFeaturesMainPageMonitor():
    try:
        response = httpx_get("http://120.27.239.120:8602")
    except Exception as e:
        success = False
        status_code = -1
        message = str(e)
    else:
        message = ""
        status_code = response.status_code
        if status_code != 200:
            success = False
        else:
            success = True
    return (success, status_code, message)


def init_monitors():
    pass  # 只是为了让这个模块上面的注册函数生效
