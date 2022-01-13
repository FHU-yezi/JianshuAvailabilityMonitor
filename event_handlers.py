from log_service import AddMonitorLog, AddRunLog
from message_service import SendFeishuMonitorFailureMessage, SendFeishuMessage
from config_service import GetConfig


def JobExecutedSuccessfully(event) -> None:
    monitor_name = event.job_id
    success, status_code, message = event.retval
    
    AddMonitorLog(monitor_name, success, status_code, message)
    if not success:
        print(f"任务出错：{message}")
        SendFeishuMonitorFailureMessage(GetConfig()["message_service"]["app_id"],
                                        GetConfig()["message_service"]["app_secret"],
                                        GetConfig()["message_service"]["email"],
                                        monitor_name, status_code, message)
        AddRunLog(3, f"发送了新的告警信息，发生错误的任务：{monitor_name}，错误码：{status_code}，错误信息：{message}")


def JobExecutedFailure(event) -> None:
    monitor_name = event.job_id
    success = False
    status_code = -2
    message = str(event.exception)
    AddMonitorLog(monitor_name, success, status_code, message)
    SendFeishuMonitorFailureMessage(GetConfig()["message_service"]["app_id"],
                                    GetConfig()["message_service"]["app_secret"],
                                    GetConfig()["message_service"]["email"],
                                    monitor_name, status_code, message)
    AddRunLog(3, f"发送了新的告警信息，发生错误的任务：{monitor_name}，错误码：{status_code}，错误信息：{message}")
