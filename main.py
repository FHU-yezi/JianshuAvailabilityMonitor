from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler

import monitors  # 不加这行会导致任务列表为空
from event_handlers import JobExecutedSuccessfully, JobExecutedFailure
from config_service import GetConfig
from log_service import AddRunLog
from message_service import SendFeishuMessage
from register import get_registered_funcs_info
from utils import CronToKwargs

AddRunLog(4, "导入模块成功")

scheduler = BackgroundScheduler()

AddRunLog(4, "初始化调度器成功")

funcs_to_schedule = get_registered_funcs_info()

AddRunLog(3, f"已注册的监控任务数量：{len(funcs_to_schedule)}")

AddRunLog(4, "开始添加监控任务")
for task_name, (func, run_cron) in funcs_to_schedule.items():
    scheduler.add_job(func, "cron", **CronToKwargs(run_cron), id=task_name)
    AddRunLog(4, f"添加监控任务：{task_name} 成功，运行 cron 表达式：{run_cron}")

AddRunLog(4, "监控任务添加完成")

AddRunLog(4, "开始注册事件回调")
scheduler.add_listener(JobExecutedSuccessfully, EVENT_JOB_EXECUTED)
scheduler.add_listener(JobExecutedFailure, EVENT_JOB_ERROR)
AddRunLog(4, "事件回调注册完成")

scheduler.start()
AddRunLog(3, "调度器启动成功")
SendFeishuMessage(GetConfig()["message_service"]["app_id"],
                  GetConfig()["message_service"]["app_secret"],
                  GetConfig()["message_service"]["email"],
                  "调度器启动成功")

while True:
    command = input("请输入命令编号：\n1. 列出所有已注册任务\n2. 停止运行\n3. 强制停止运行\n>>>")

    if command == "1":
        for x in scheduler.get_jobs():
            print(x)  # 分行输出
    elif command == "2":
        if input("确认停止运行吗？(y/n)\n>>>") == "y":
            print("请等待任务执行完毕......")
            AddRunLog(4, "已发起停止请求")
            scheduler.shutdown()
            AddRunLog(3, "调度器已停止")
            SendFeishuMessage(GetConfig()["message_service"]["app_id"],
                              GetConfig()["message_service"]["app_secret"],
                              GetConfig()["message_service"]["email"],
                              "调度器已停止")
            print("已安全停止运行")
            exit()
    elif command == "3":
        print("强制停止运行可能导致数据库异常，请谨慎操作")
        if input("确认强制停止运行吗？(y/n)\n>>>") == "y":
            scheduler.shutdown(wait=False)  # 不等待任务执行完毕
            AddRunLog(2, "调度器已强制停止")
            SendFeishuMessage(GetConfig()["message_service"]["app_id"],
                              GetConfig()["message_service"]["app_secret"],
                              GetConfig()["message_service"]["email"],
                              "调度器已强制停止")
            print("已强制停止运行")
            exit()
    elif command == "":
        continue  # 直接按下回车将重新输出提示信息
    else:
        print("指令无效，请检查")
