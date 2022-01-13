from log_service import AddMonitorLog, AddRunLog, IsFailedUntilNow
from message_service import SendFeishuMonitorFailureMessage, SendFeishuReAvailableMessage
from config_service import GetConfig


def JobExecutedSuccessfully(event) -> None:
    monitor_name = event.job_id
    success, status_code, message = event.retval

    if not success:
        print(f"任务出错：{message}")
        if IsFailedUntilNow(monitor_name):
            # 告警信息已经发送过
            AddRunLog(4, f"跳过告警信息发送，因为 {monitor_name} 的告警信息已经发送过")
        else:
            SendFeishuMonitorFailureMessage(GetConfig()["message_service"]["app_id"],
                                            GetConfig()["message_service"]["app_secret"],
                                            GetConfig()["message_service"]["email"],
                                            monitor_name, status_code, message)
            AddRunLog(3, f"发送了新的告警信息，发生错误的任务：{monitor_name}，错误码：{status_code}，错误信息：{message}")
    else:  # 任务执行成功
        if IsFailedUntilNow(monitor_name):  # 服务恢复
            SendFeishuReAvailableMessage(GetConfig()["message_service"]["app_id"],
                                         GetConfig()["message_service"]["app_secret"],
                                         GetConfig()["message_service"]["email"],
                                         monitor_name)
    AddMonitorLog(monitor_name, success, status_code, message)


def JobExecutedFailure(event) -> None:
    monitor_name = event.job_id
    success = False
    status_code = -2
    message = str(event.exception)

    if IsFailedUntilNow(monitor_name):
        # 告警信息已经发送过
        AddRunLog(4, f"跳过告警信息发送，因为 {monitor_name} 的告警信息已经发送过")
    else:
        SendFeishuMonitorFailureMessage(GetConfig()["message_service"]["app_id"],
                                        GetConfig()["message_service"]["app_secret"],
                                        GetConfig()["message_service"]["email"],
                                        monitor_name, status_code, message)
        AddRunLog(3, f"发送了新的告警信息，发生错误的任务：{monitor_name}，错误码：{status_code}，错误信息：{message}")
    AddMonitorLog(monitor_name, success, status_code, message)
