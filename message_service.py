from typing import Union
from datetime import datetime

from httpx import post as httpx_post

from log_service import AddRunLog


def SendFeishuMessage(app_id: str, app_secret: str, email: str, message: str) -> None:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data_to_get_token = {"app_id": app_id, "app_secret": app_secret}
    headers["Authorization"] = "Bearer " + httpx_post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", headers=headers, json=data_to_get_token).json()["tenant_access_token"]

    data_to_send_message = {"email": email, "msg_type": "text", "content": {"text": message}}
    response = httpx_post("https://open.feishu.cn/open-apis/message/v4/send/", headers=headers, json=data_to_send_message)
    if response.json()["code"] != 0:
        AddRunLog(1, f"向{email}发送飞书消息失败，错误码：{response.json()['code']}")
    else:
        AddRunLog(3, f"向{email}发送飞书消息成功，消息代码：{response.json()['data']['message_id']}")


def SendFeishuMonitorFailureMessage(app_id: str, app_secret: str, email: str, task_name: str, status_code: int, message: Union[str, None]) -> None:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data_to_get_token = {"app_id": app_id, "app_secret": app_secret}
    headers["Authorization"] = "Bearer " + httpx_post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", headers=headers, json=data_to_get_token).json()["tenant_access_token"]

    data_to_send_message = {
        "email": email,
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "监控预警"
                },
                "template": "red"
            },
            "elements": [{
                "tag": "markdown",
                "content": f"**时间：**{datetime.now()}\n**任务名称：**{task_name}\n**状态码：**{status_code}\n**错误信息：**{message}"
            }]
        }
    }

    response = httpx_post("https://open.feishu.cn/open-apis/message/v4/send/", headers=headers, json=data_to_send_message)
    if response.json()["code"] != 0:
        AddRunLog(1, f"向{email}发送监控预警飞书消息失败，错误码：{response.json()['code']}")
    else:
        AddRunLog(3, f"向{email}发送监控预警飞书消息成功，消息代码：{response.json()['data']['message_id']}")


def SendFeishuReAvailableMessage(app_id: str, app_secret: str, email: str, task_name: str) -> None:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data_to_get_token = {"app_id": app_id, "app_secret": app_secret}
    headers["Authorization"] = "Bearer " + httpx_post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", headers=headers, json=data_to_get_token).json()["tenant_access_token"]

    data_to_send_message = {
        "email": email,
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "服务恢复"
                },
                "template": "green"
            },
            "elements": [{
                "tag": "markdown",
                "content": f"**时间：**{datetime.now()}\n**任务名称：**{task_name}"
            }]
        }
    }

    response = httpx_post("https://open.feishu.cn/open-apis/message/v4/send/", headers=headers, json=data_to_send_message)
    if response.json()["code"] != 0:
        AddRunLog(1, f"向{email}发送服务恢复飞书消息失败，错误码：{response.json()['code']}")
    else:
        AddRunLog(3, f"向{email}发送服务恢复飞书消息成功，消息代码：{response.json()['data']['message_id']}")
